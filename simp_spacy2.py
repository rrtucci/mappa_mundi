"""

This file contains one of several implementations of the function
`simplify_ztz(sentence, verbose=False)` that we considered.

Refs:

https://spacy.io/usage/spacy-101/

https://github.com/ac491/Sentence-simplifier/blob/master/simplifcation.ipynb
"""
import spacy
import nltk

nltk.download('averaged_perceptron_tagger')

nlp = spacy.load("en_core_web_sm")

# set of relative pronouns
RELPRON = ['whom', 'whose', 'which', 'who']


def transform(parsed):
    d = {}
    # print(parsed)
    # print()
    for x in parsed:
        rel = x.dep_
        parent = x.head.i + 1
        dependent = x.i + 1
        if parent == dependent and rel == 'ROOT':
            parent = 0
        if parent not in d.keys():
            d[parent] = {}
        if rel not in d[parent].keys():
            d[parent][rel] = []

        d[parent][rel].append(dependent)

    return d


def analyse_rc(sentence):
    # check for markers indicating rel_clause
    if any([s.lower() in RELPRON for s in sentence]):
        mark = []
        for s in sentence:
            if s.lower() in RELPRON:
                mark.append(s.lower())
        return True, mark
    else:
        return False, None


def remove_all(aux, item):
    for a in aux.keys():
        for d in aux[a].keys():
            if item in aux[a][d]:
                aux[a][d].remove(item)


def build(root, dep, aux, words, final, yes_root=True, previous=None):
    if previous == None:
        previous = []

    if root in previous:
        return

    previous.append(root)

    if yes_root:
        final[root] = words[root - 1]
        previous.append(root)

    for k in dep.keys():
        for i in dep[k]:
            if i in aux.keys():
                deps = aux[i]
                build(i, deps, aux, words, final, previous=previous)

            final[i] = words[i - 1]


def appositive_phrases(dep_dict, words, root, dep_root, ant):
    if 'nsubj' in dep_root:
        subj = dep_root['nsubj'][0]
        subj_word = words[subj - 1]

        # print(dep_dict)
        if subj not in dep_dict:
            return False, ant

        deps_subj = dep_dict[subj]
        v_tense = words[root - 1][1]
        n_num = words[subj - 1][1]

        if 'amod' in deps_subj:
            mod = deps_subj['amod'][0]
            if mod in dep_dict:
                deps_mod = dep_dict[mod]
            else:
                deps_mod = {}
            del dep_dict[subj]['amod']
            deps_subj = dep_dict[subj]

            ## Treat simple cases such as 'general rule'
            if 'JJ' in words[mod - 1][1] and 'punct' not in deps_subj:
                return False, ant

        elif 'appos' in deps_subj:
            mod = deps_subj['appos'][0]
            if mod in dep_dict:
                deps_mod = dep_dict[mod]
            else:
                deps_mod = {}
            del dep_dict[subj]['appos']
            deps_subj = dep_dict[subj]
        else:
            return False, ant

        if 'punct' in deps_subj.keys():
            del deps_subj['punct']

        final_root = {}
        build(root, dep_root, dep_dict, [s[0].lower() for s in words],
              final_root)
        final_appos = {}
        build(mod, deps_mod, dep_dict, [s[0].lower() for s in words],
              final_appos)
        final_subj = {}
        build(subj, deps_subj, dep_dict, [s[0].lower() for s in words],
              final_subj)

        # print(final_root)
        s1 = []
        for i in sorted(final_root):
            s1.append(final_root[i])
        s1 = ' '.join(s1)
        # print(s1)

        # print(final_appos)
        s2 = []
        for i in sorted(final_appos):
            s2.append(final_appos[i])
        s2 = ' '.join(s2)
        # print(s2)

        # print(final_subj)
        s3 = []
        for i in sorted(final_subj):
            s3.append(final_subj[i])
        s3 = ' '.join(s3)
        # print(s3)

        if len(final_appos.keys()) < 2:
            return False, ant

        if n_num in ["NN", "NNP"]:
            if v_tense in ["VBP", "VBZ", "VB"]:
                s3 += " is "
            elif v_tense in ["VBD", "VBG", "VBN"]:
                s3 += " was "

        elif n_num in ["NNS", "NNPS"]:
            if v_tense in ["VBP", "VBZ", "VB"]:
                s3 += " are "
            elif v_tense in ("VBD", "VBG", "VBN"):
                s3 += " were "

        elif n_num in ["PRP"] and subj_word.lower() == "they":

            if v_tense in ["VBP", "VBZ", "VB"]:
                s3 += " are "
            elif v_tense in ["VBD", "VBG", "VBN"]:
                s3 += " were "

        elif n_num in ["PRP"]:
            if v_tense in ["VBP", "VBZ", "VB"]:
                s3 += " is "
            elif v_tense in ["VBD", "VBG", "VBN"]:
                s3 += " was "

        s2 = s3 + s2

        return True, [s1, s2]

    return False, ant


def relative_clauses(dep_dict, words, root, dep_root, rel, ant):
    subj = dep_root[rel][0]
    if subj in dep_dict:

        dep_subj = dep_dict[subj]

        if 'relcl' in dep_subj or 'rcmod' in dep_subj:
            if 'relcl' in dep_subj:
                relc = dep_subj['relcl'][0]
                type_rc = 'relcl'
            else:
                relc = dep_subj['rcmod'][0]
                type_rc = 'rcmod'
            deps_relc = dep_dict[relc]

            if 'nsubj' in deps_relc:
                subj_rel = 'nsubj'
            elif 'nsubjpass' in deps_relc:
                subj_rel = 'nsubjpass'

            if 'ref' in dep_subj:
                to_remove = dep_subj['ref'][0]
                mark = words[dep_subj['ref'][0] - 1].lower()
            else:
                to_remove = deps_relc[subj_rel][0]
                mark = words[deps_relc[subj_rel][0] - 1].lower()

            # print(mark)

            if mark in RELPRON:
                deps_relc[subj_rel][0] = subj
                remove_all(dep_dict, to_remove)
            elif 'dobj' in deps_relc:  ## needed for cases where the subject of the relative clause is the object
                obj = deps_relc['dobj'][0]

                if 'poss' in dep_dict[obj]:
                    mod = dep_dict[obj]['poss'][0]
                    aux_words = words[mod - 1]
                    aux_words = words[subj - 1] + '\'s'
                    words[mod - 1] = aux_words
                    dep_dict[mod] = dep_dict[subj]
                else:
                    return False, ant
            else:
                return False, ant  # for borken cases - " There are some situations where it is particularly important that you get financial information and advice that is independent of us."

            del dep_dict[subj][type_rc]

            if 'punct' in dep_subj:
                del dep_dict[subj]['punct']

            final_root = {}
            build(root, dep_root, dep_dict, words, final_root)
            final_relc = {}
            build(relc, deps_relc, dep_dict, words, final_relc)

            # print(final_root)
            # print(final_relc)

            s1 = []
            for i in sorted(final_root):
                s1.append(final_root[i])

            s2 = []
            for i in sorted(final_relc):
                s2.append(final_relc[i])

            return True, [' '.join(s1), ' '.join(s2)]
    return False, ant


sentence0 = 'Robert, who lives nearby, was walking his dog'
sentence1 = 'Marcus, my sister\'s hamster, likes to run in a wheel.'


def simplify_ztz(ztz, verbose=False):
    """
    This method simplifies the sentence `ztz`.

    Parameters
    ----------
    sentence: str
    verbose: bool

    Returns
    -------
    str

    """
    ztz.strip()
    sentences = [ztz]
    result = []

    for s in sentences:

        output = nlp(s)

        dep_dict = transform(output)
        # print(dep_dict)

        # words = [(token.text.lower(), token.pos_) for token in output]

        tokens = [token.text.lower() for token in output]

        words = nltk.pos_tag(tokens)

        # print(words)

        if 0 in dep_dict:

            root = dep_dict[0]['ROOT'][0]

            if root in dep_dict:

                dep_root = dep_dict[root]

                # handle appositive_phrases
                flag_appos, res = appositive_phrases(dep_dict, words, root,
                                                     dep_root, sentences)
                if flag_appos:
                    result += res
                    continue

                # check for relative clauses
                flag_rc, type_rc = analyse_rc(s.split())

                if flag_rc:

                    if 'nsubj' in dep_root:
                        flag, res = relative_clauses(dep_dict, tokens, root,
                                                     dep_root, 'nsubj',
                                                     sentences)
                        if flag:
                            result += res
                            continue
                    elif 'dobj' in dep_root:
                        flag, res = relative_clauses(dep_dict, tokens, root,
                                                     dep_root, 'dobj',
                                                     sentences)
                        if flag:
                            result += res
                            continue
        result.append(s)

    if verbose:
        print(ztz.strip())
        print(result)
