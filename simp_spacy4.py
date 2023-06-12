"""

This file contains one of several implementations of the function
`simplify_ztz(sentence, verbose=False)` that we considered.

References:

 1. "Knowledge graphs from complex text" by Karthika Vijayan (Solution
    Consultant @Sahaj )
    https://medium.com/inspiredbrilliance/knowledge-graphs-from-complex-text-eb009aeed48e

"""
import spacy
nlp = spacy.load('en_core_web_lg')
import coreferee
import spacy_transformers

def coref_resolve(text):
    nlp1 = spacy.load('en_core_web_trf')
    nlp1.add_pipe('coreferee')
    doc1 = nlp1(text)
    tok_list = list(token.text for token in doc1)
    c = 0
    for chain in doc1._.coref_chains:
        for mention in chain:
            res1 = [doc1._.coref_chains.resolve(doc1[i]) for i in mention]
            res = list(filter((None).__ne__, res1))
            if len(res) != 0:
                if len(res[0]) == 1:
                    tok_list[mention[0] + c] = str(res[0][0])
                elif len(res[0]) > 1:
                    tok_list[mention[0] + c] = str(res[0][0])
                    for j in range(1, len(res[0])):
                        tok_list.insert(mention[0] + c + j, str(res[0][j]))
                        c = c + 1
    textres = " ".join(tok_list)
    return textres


def compound_to_simple(sentence):
    doc = nlp(sentence)

    root_token = None
    for token in doc:
        if (token.dep_ == "ROOT"):
            root_token = token

    other_verbs = []
    for token in doc:
        ancestors = list(token.ancestors)
        if (token.pos_ == "VERB" and len(
                ancestors) < 3 and token != root_token):
            other_verbs.append(token)

    token_spans = []
    all_verbs = [root_token] + other_verbs
    for other_verb in all_verbs:
        first_token_index = len(doc)
        last_token_index = 0
        this_verb_children = list(other_verb.children)
        for child in this_verb_children:
            if (child not in all_verbs):
                if (child.i < first_token_index):
                    first_token_index = child.i
                if (child.i > last_token_index):
                    last_token_index = child.i
        token_spans.append((first_token_index, last_token_index))

    sentence_clauses = []
    for token_span in token_spans:
        start = token_span[0]
        end = token_span[1]
        if (start < end):
            clause = doc[start:end]
            sentence_clauses.append(clause)
    sentence_clauses = sorted(sentence_clauses, key=lambda tup: tup[0])
    clauses_text = [clause.text for clause in sentence_clauses]
    return clauses_text

def simplify_ztz(sentence, verbose=False):
    """
    This method simplifies the sentence `sentence`.

    Parameters
    ----------
    sentence: str
    verbose: bool

    Returns
    -------
    str

    """
    textres = coref_resolve(sentence)
    ztz_list = compound_to_simple(textres)
    if verbose:
        print(sentence.strip())
        print(ztz_list)
    return ztz_list