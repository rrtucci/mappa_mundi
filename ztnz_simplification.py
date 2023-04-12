"""
https://github.com/garain/Sentence-Simplification
zntz = sentence

"""
import nltk
from nltk.tree import ParentedTree
from anytree import NodeMixin, Node, AnyNode, RenderTree
import re
import os
import subprocess
from my_globals import *

version = subprocess.check_output(
    ['java', '-version'], stderr=subprocess.STDOUT)
print("java version=\t", version)
print("CLASSPATH=\t", os.environ['CLASSPATH'])
print("STANFORD_MODELS=\t", os.environ['STANFORD_MODELS'])
print("JAVA_HOME=\t", os.environ['JAVA_HOME'])

from nltk.parse.stanford import StanfordParser
parser = StanfordParser()

def simplify_zntz(sentence0, verbose=False):
    simple_ztnz_list = []

    # split = []
    # simple_sent = []
    # index = []
    # index1 = 0
    n = 0
    but = 0
    # scount = 0
    # parts = []
    # ht_3_last_obj = []


    def SBAR_simplify(sent):

        def make_tree(tree, t, sent_list):
            # this fn. converts nltk tree to anytree
            if tree not in sent_list:
                ttt = AnyNode(id=str(tree.label()), parent=t)
                for tt in tree:
                    make_tree(tt, ttt, sent_list)
            else:
                AnyNode(id=str(tree), parent=t)

        # SBAR CASE
        def find_sbar(t):
            if t.id == 'SBAR':
                global sbar
                sbar = t
            for tt in t.children:
                find_sbar(tt)

        def find_vp_in_sbar(t):
            if t.id == 'VP':
                global vp_sbar
                vp_sbar.append(t)
            for tt in t.children:
                find_vp_in_sbar(tt)

        def find_np_in_sbar(t):
            global f
            global ff
            if t.id == 'VP':
                ff = False
            if (t.id == 'NP') and f == True and ff == True:
                global np_sbar
                np_sbar = t
                f = False
            for tt in t.children:
                find_np_in_sbar(tt)

        def find_vp(t):
            if t.id == 'SBAR':
                return
            global f
            if t.id == 'VP' and f == True:
                global vp
                vp = t
                f = False
            for tt in t.children:
                find_vp(tt)

        def find_np(t):
            if t.id == 'SBAR':
                return
            global f
            if t.id == 'NP' and f == True:
                global np
                np = t
                f = False
            for tt in t.children:
                find_np(tt)

        def find_vbz(t):
            if t.id == 'SBAR':
                return
            global f
            if t.id == 'VBZ' and f == True:
                global vbz
                vbz = t.children[0].id
                f = False
            for tt in t.children:
                find_vbz(tt)

        def make_sent(t):
            global simple_sentences
            if t.id in sent_list:
                simple_sentences[-1].append(t.id)
            for tt in t.children:
                make_sent(tt)

        # sent=sent8

        parse_trees = parser.raw_parse(sent)
        global sent_list
        sent_list = [s for s in sent.split()]
        tree = next(parse_trees)[0]
        # tree.draw()
        t = AnyNode(id='ROOT')
        make_tree(tree, t, sent_list)
        global sbar
        sbar = t
        global vp_sbar
        global f
        global ff
        global np_sbar
        global vp
        global np
        global vbz
        vp_sbar = []
        vp = t
        np = t
        vbz = 'bn2'
        np_sbar = t
        find_sbar(t)
        find_vp_in_sbar(sbar)
        f = True
        ff = True
        find_np_in_sbar(sbar)
        f = True
        find_vp(t)
        f = True
        find_np(t)
        f = True
        find_vbz(t)
        global simple_sentences
        simple_sentences = []
        simple_sentences.append([])
        make_sent(np)
        make_sent(vp)
        for i in range(len(vp_sbar)):
            simple_sentences.append([])
            if np_sbar == t:
                make_sent(np)
            else:
                make_sent(np_sbar)
            if vbz != 'bn2':
                simple_sentences[-1].append(vbz)
            make_sent(vp_sbar[i])
        # print (simple_sentences)
        simple = []
        for sentence in simple_sentences:
            string = ''
            for word in sentence:
                string += word + ' '
            string += '.'
            simple.append(string)

        def is_any_sbar(t):
            if t.id == 'SBAR':
                global f
                f = True
                return
            for tt in t.children:
                is_any_sbar(tt)

        f = False
        is_any_sbar(t)
        if f == False:
            simple = [sent]
        return simple

    # print(pos_tagged)
    # SBAR functions start here
    def make_tree_sbar(tree, t, sent_list):
        # this fn. converts nltk tree to anytree
        if tree not in sent_list:
            ttt = AnyNode(id=str(tree.label()), parent=t)
            for tt in tree:
                make_tree_sbar(tt, ttt, sent_list)
        else:
            AnyNode(id=str(tree), parent=t)


    def find_sbar(t):
        if t.id == 'SBAR':
            global sbar
            sbar = t
        for tt in t.children:
            find_sbar(tt)


    def find_vp_in_sbar(t):
        if t.id == 'VP':
            global vp_sbar
            vp_sbar = t
        for tt in t.children:
            find_vp_in_sbar(tt)


    def find_vp(t):
        if t.id == 'SBAR':
            return
        global f
        if t.id == 'VP' and f == True:
            global vp
            vp = t
            f = False
        for tt in t.children:
            find_vp(tt)


    def find_np(t):
        if t.id == 'SBAR':
            return
        global f
        if t.id == 'NP' and f == True:
            global np
            np = t
            f = False
        for tt in t.children:
            find_np(tt)


    def find_vbz(t):
        if t.id == 'SBAR':
            return
        global f
        if t.id == 'VBZ' and f == True:
            global vbz
            vbz = t.children[0].id
            f = False
        for tt in t.children:
            find_vbz(tt)


    def make_sent(t):
        global simple_sentences
        if t.id in sent_list:
            simple_sentences[-1].append(t.id)
        for tt in t.children:
            make_sent(tt)


    # SBAR functions end here
    # Multiple CC functions start here
    def pos_tag(tokenized_sent):
        return nltk.pos_tag(tokenized_sent)


    def has_conj(tagged_sent):
        cc_list = [('and', 'CC'), ('but', 'CC')]
        for cc_pair in cc_list:
            if cc_pair in tagged_sent:
                return True
        return False


    def split_needed(sent_list):
        for sent in sent_list:
            if has_conj(pos_tag(tokenize(sent))):
                return True
        return False


    def do_split(sent, cc_tuple):
        pos_tagged = pos_tag(tokenize(sent))
        tree = next(parser.tagged_parse(pos_tagged))
        tree1 = ParentedTree.convert(tree)
        # tree.draw()
        count = 0
        m = 0
        for t in tree1.subtrees():
            if t.label() == 'PP':
                count = count + 1

        index = []
        index1 = 0
        if count > 0 and (('to') not in tokenized_sent and (
        'washed') not in tokenized_sent) and (tokenized_sent.count(",") < 2):
            for i in range(len(pos_tagged) - 3):
                if (pos_tagged[i][1] == 'VBD' or pos_tagged[i][1] == 'VBZ') and \
                        pos_tagged[i + 1][1] != 'VBG' and pos_tagged[i + 3][
                    1] != 'CC' and pos_tagged[i + 1][1] != 'NNP' and \
                        pos_tagged[i - 1][1] != 'CC':
                    pos_tagged.insert(i + 1, (',', ','))

            for j in range(len(pos_tagged)):
                if pos_tagged[j][1] == 'CC':
                    index.append(j)

        for t in tree1.subtrees():
            if t.label() == 'SBAR':
                m = m + 1
        if len(index) > 0 and count > 0 and m == 0:
            c = 0
            for i in range(len(index)):
                pos_tagged.insert(index[i] + c, (',', ','))
                c = c + 1
        if m > 0:
            for j in range(len(pos_tagged)):
                if pos_tagged[j][1] == 'CC':
                    index1 = j

        if (index1 > 0 and m > 0) and count == 0:
            pos_tagged.insert(index1, (' ,', ','))  # ', 'is used
            pos_tagged.insert(index1 + 2, (', ', ','))  # ' ,' is used
        # print(pos_tagged)
        tree = next(parser.tagged_parse(pos_tagged))
        p_tree = ParentedTree.convert(tree)

        leaf_values = p_tree.leaves()
        parts = []
        ht_3_last_obj = []

        if cc_tuple in pos_tagged:
            leaf_index = leaf_values.index(cc_tuple[0])
            tree_location = p_tree.leaf_treeposition(leaf_index)
            parent = p_tree[tree_location[:-2]]
            # print(parent.height())

            if parent.height() == 3:
                # find the noun being referred to
                for subtree in reversed(list(parent.subtrees())):
                    if subtree.parent() == parent:
                        if subtree.label() == 'NN' or subtree.label() == 'NNS':
                            ht_3_last_obj = subtree.leaves() + ht_3_last_obj
                            del p_tree[subtree.treeposition()]
                # print("ht 3 last obj -> ", ht_3_last_obj)
                part = []
                for subtree in reversed(list(parent.subtrees())):
                    if subtree.parent() == parent:
                        # print(subtree)
                        if subtree.label() != ',' and subtree.label() != 'CC':
                            part = subtree.leaves() + part
                        else:
                            parts.append(part + ht_3_last_obj)
                            part = []
                        del p_tree[subtree.treeposition()]
                parts.append(part + ht_3_last_obj)
                # print('parent', parent)
                # print('treeloc', tree_location)
                parent.append(ParentedTree('INSRT', ['*']))

            else:
                for subtree in reversed(list(parent.subtrees())):
                    if subtree.parent() == parent:
                        # print(subtree)
                        if subtree.label() != ',' and subtree.label() != 'CC':
                            parts.append(subtree.leaves() + ht_3_last_obj)
                        del p_tree[subtree.treeposition()]
                # print('parent', parent)
                # print('treeloc', tree_location)
                parent.append(ParentedTree('INSRT', ['*']))

        # p_tree.draw()
        # print(parts)

        split = []
        rem = p_tree.leaves()
        start_idx = rem.index('*')

        for part in reversed(parts):
            offset = start_idx
            r_clone = rem.copy()
            del r_clone[offset]
            for i, word in enumerate(part):
                r_clone.insert(offset + i, word)
            split.append(r_clone)

        # print("split", split)

        split = [" ".join(sent) for sent in split]

        return split


    def split_util(sent):
        cc_list = [('and', 'CC'), ('but', 'CC')]
        for cc_pair in cc_list:
            if cc_pair in pos_tag(tokenize(sent)):
                return do_split(sent, cc_pair)
        return sent


    def rem_dup(list):
        final = []
        for item in list:
            if item not in final:
                final.append(item)
        return final


    def simplify(sent):
        initial = [sent]
        final = []

        while (split_needed(initial)):
            final = []
            while (initial):
                sent = initial.pop(0)
                if (split_needed([sent])):
                    for split_sent in reversed(split_util(sent)):
                        final.append(split_sent)
                else:
                    final.append(sent)
            # print("final -> ", final)
            initial = final.copy()

        final = rem_dup(final)
        final = list(reversed(final))
        # print(final)

        return final


    def tokenize(sent):
        tokenized_sent = nltk.word_tokenize(sent)
        if ('If') in tokenized_sent and ('then') in tokenized_sent:
            tokenized_sent.remove('If')
            tokenized_sent.insert(tokenized_sent.index('then'), 'and')
            tokenized_sent.remove('then')
        if ('because') in tokenized_sent:
            tokenized_sent.insert(tokenized_sent.index('because'),
                                  (','))  # ', 'is used
            tokenized_sent.insert(tokenized_sent.index('because') + 1, (','))
            tokenized_sent.insert(tokenized_sent.index('because'), 'and')
            tokenized_sent.remove('because')
        if ('while') in tokenized_sent:
            tokenized_sent.insert(tokenized_sent.index('while'), 'and')
            tokenized_sent.remove('while')
        if ('which') in tokenized_sent:
            tokenized_sent.insert(tokenized_sent.index('which'), 'and')
            tokenized_sent.remove('which')
        if ('or') in tokenized_sent:
            tokenized_sent.insert(tokenized_sent.index('or'), 'and')
            tokenized_sent.remove('or')
        if ('who') in tokenized_sent:
            while (',') in tokenized_sent:
                tokenized_sent.insert(tokenized_sent.index(','), 'and')
                tokenized_sent.remove(',')
            tokenized_sent.insert(tokenized_sent.index('who'), 'and')
            tokenized_sent.remove('who')

        return tokenized_sent

    sentences = [sentence0.strip()]
    for sentence in sentences:
        if verbose:
            print("Complex Sentence: " + sentence)
        tokenized_sent = tokenize(sentence)
        # print(tokenized_sent)

        # parse_trees = parser1.tagged_parse(pos_tagged)

        pos_tagged = pos_tag(tokenized_sent)
        parse_trees = parser.tagged_parse(pos_tagged)
        tree = next(parse_trees)
        p_tree = ParentedTree.convert(tree)
        # p_tree.draw()

        leaf_values = p_tree.leaves()
        # print(leaf_values)
        for i in pos_tagged:
            if ('and') in i:
                n = n + 1

            if ('but') in i:
                but = but + 1
        tree1 = ParentedTree.convert(tree)
        # tree.draw()
        m = 0
        for t in tree1.subtrees():
            if t.label() == 'SBAR':
                m = m + 1

        if (n + but) > 0:
            # tokenized_sent=nltk.word_tokenize(sent10)
            # pos_tagged=nltk.pos_tag(tokenized_sent)
            sent1 = sentence
            sent = " ".join(tokenize(sent1))
            # print(sent)
            simplified = simplify(sent)
            for i in simplified:
                i = list(i)
                if ord(i[0]) >= 97 and ord(i[0]) <= 122:
                    i[0] = chr(ord(i[0]) - 32)
                while i.count(",") > 0:
                    # i.pop(i.index(","))
                    del (i[i.index(",")])
                if (".") not in (i):
                    if verbose:
                        print("Simple sentence: " + "".join(i) + ".")
                    simple_ztnz_list.append("".join(i) + ".")
                else:
                    if verbose:
                        print("Simple sentence: " + "".join(i))
                    simple_ztnz_list.append("".join(i))
            n = 0
            but = 0
            # print("."),

        elif n == 0 and m > 0 and len(re.findall(r",", sentence)) == 0 and len(
                re.findall(r"While", sentence)) == 0:
            try:
                sent = sentence
                # print(sent)
                # print("Hello")
                tokenized_sent = tokenize(sent)
                pos_tagged = nltk.pos_tag(tokenized_sent)
                parse_trees = parser.tagged_parse(pos_tagged)
                sent_list = [s for s in sent.split()]
                tree = next(parse_trees)[0]
                # tree.draw()
                t = AnyNode(id='ROOT')
                make_tree_sbar(tree, t, sent_list)
                sbar = t
                vp_sbar = t
                vp = t
                np = t
                vbz = 'asvf'
                find_sbar(t)
                find_vp_in_sbar(sbar)
                f = True
                find_vp(t)
                f = True
                find_np(t)
                f = True
                find_vbz(t)
                simple_sentences = []
                simple_sentences.append([])
                make_sent(np)
                make_sent(vp)
                simple_sentences.append([])
                make_sent(np)
                if vbz != 'asvf':
                    simple_sentences[-1].append(vbz)
                make_sent(vp_sbar)
                for i in simple_sentences:
                    i = list(i)

                    #             if ord(i[0])>=97 and ord(i[0])<=122:
                    #                i[0]=chr(ord(i[0])-32)

                    while i.count(",") > 0:
                        i.pop(i.index(","))
                    if (".") not in (i):
                        if verbose:
                            print("Simple sentence: " + " ".join(i) + ".")
                        simple_ztnz_list.append(" ".join(i) + ".")
                    else:
                        if verbose:
                            print("Simple sentence: " + " ".join(i))
                        simple_ztnz_list.append(" ".join(i))
                # print("."),
            except:
                continue
        elif m > 0 and (len(re.findall(r",", sentence)) > 0 or len(
                re.findall(r"While", sentence)) > 0):
            try:
                # sent=re.sub(r",","",sentence)
                # print("Hello")
                tokenized_sent = tokenize(sentence)
                simple_sentences = SBAR_simplify(" ".join(tokenized_sent))
                for i in simple_sentences:
                    # i=list(i)

                    #             if ord(i[0])>=97 and ord(i[0])<=122:
                    #                i[0]=chr(ord(i[0])-32)

                    # while i.count(",")>0:
                    #  i.pop(i.index(","))
                    if (".") not in (i):
                        if verbose:
                            print("Simple sentence: " + i)
                        simple_ztnz_list.append(i)
                    else:
                        if verbose:
                            print("Simple sentence: " + i)
                        simple_ztnz_list.append(i)
                # print("."),
            except:
                continue
    return [zntz for zntz in simple_ztnz_list if len(zntz)>2]

def simplify_one_m_script(
    in_dir, out_dir,
    file_name):
    inpath = in_dir + "/" + file_name
    outpath = out_dir + "/" + file_name
    new_lines = []
    with open(inpath, "r", encoding="utf-8") as f:
        count = 1
        for line in f:
            print(count)
            simple_ztnz_list = simplify_zntz(line)
            new_lines.append(ZNTZ_SEPARATOR.join(simple_ztnz_list))
            count += 1
    with open(outpath, "w", encoding="utf-8") as f:
        for line in new_lines:
            f.write(line + "\n")


def simplify_batch_of_m_scripts(
        in_dir, out_dir,
        batch_file_names):
    all_file_names = os.listdir(in_dir)
    assert set(batch_file_names).issubset(set(all_file_names))
    for file_name in batch_file_names:
        i = all_file_names.index(file_name)
        print('%i.' % (i + 1), file_name)
        simplify_one_m_script(in_dir, out_dir, file_name)


if __name__ == "__main__":
    def main1():
        path = "All_types_of_inputs.txt"
        with open(path, "r") as f:
            count = 1
            for line in f:
                print(count, ".")
                simplify_zntz(line, verbose=True)
                count += 1
    def main2():
        in_dir = "short_stories_prep"
        out_dir = "short_stories_simp"
        batch_file_names = os.listdir(in_dir)[1:2]
        simplify_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names)
    def main3():
        remove_dialogs = True
        in_dir = PREP_DIR if not remove_dialogs else PREP_RD_DIR
        out_dir = SIMP_DIR if not remove_dialogs else SIMP_RD_DIR
        batch_file_names = os.listdir(in_dir)[0:2]
        simplify_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names)

    main1()
    # main2()
