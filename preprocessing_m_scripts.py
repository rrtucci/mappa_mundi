"""
https://www.datacamp.com/tutorial/python-regular-expression-tutorial

"""
import re
import os
from nltk import tokenize
import collections as co
from my_globals import *


def preprocess_one_m_script(in_dir,
                            out_dir,
                            file_name,
                            remove_dialog=False):
    print('fetching %s' % file_name)
    def count_leading_wh_sp(str0):
        # wh_sp = white space
        count = 0
        if str0:
            for char in str0:
                if char.isspace():
                    count += 1
                else:
                    break
        return count

    inpath =  in_dir + "/" + file_name
    outpath = out_dir + "/" + file_name

    with open(inpath, "r", encoding='utf-8') as f:
        lines = [line for line in f]

    # strip trailing (i.e., right) white space and newline.
    # If this results in an empty line, remove it.
    new_lines =[]
    for line in lines:
        line = line.rstrip()
        if line:
            new_lines.append(line)
    lines = new_lines

    # remove everything after and including THE END
    new_lines = []
    for line in lines:
        if line.strip() in ["THE END", "END"]:
            break
        else:
            new_lines.append(line)
    lines = new_lines

    # regex for parenthetical remarks
    pattern_par = re.compile(r'\[(.*?)\]|\((.*?)\)|\{(.*?)\}')

    # Substitutions. If this results in empty line,
    # remove it.
    new_lines = []
    for line in lines:
        # print("ssdf", line)
        # remove parenthetical remarks
        line = re.sub(pattern_par, "", line)
        # Replace tabs by 12 blank spaces
        line = re.sub(r"\t", " "*12, line)
        # print("\tssdf", line)
        if len(line)>=1:
            new_lines.append(line)
    lines = new_lines

    # Add missing periods for transitions from dialog to narration or vice
    # versa
    indent = count_leading_wh_sp(lines[0])
    for i in range(len(lines)):
        if i != len(lines)-1:
            next_indent = count_leading_wh_sp(lines[i+1])
            if indent != next_indent and \
                    not lines[i][-1] in [".", "!", "?"]:
                lines[i] = lines[i] + "."
        else:
            next_indent = None
            if not lines[i][-1] in [".", "!", "?"]:
                lines[i] = lines[i] + "."
        indent = next_indent

    # Regex for string that contains at least 2 lower case letters
    # Got cases where line was just "is."
    pattern_lc = re.compile(r'^(.*[a-z]){2,}.*$')

    # Reject lines that don't contain at least 2 lower case letters string.
    # This gets rid of scene directions and character invocations.
    lines = [line for line in lines if re.search(pattern_lc, line)]

    white_spaces = [count_leading_wh_sp(line) for line in lines]
    wh_sp_counter = co.Counter(white_spaces)
    # print("llkh", wh_sp_counter)
    sum_reps = sum(wh_sp_counter.values())
    indent_prob_dist = co.OrderedDict()
    indents = []
    for indent in sorted(wh_sp_counter,
                       key=wh_sp_counter.get,
                       reverse=True):
        prob = round(wh_sp_counter[indent]/sum_reps, 3)
        indent_prob_dist[indent]= prob
        indents.append(indent)
    # print("ddfg", indents)
    # print("ddfg", indent_prob_dist)
    print("\tindent prob dist =", [(indent, indent_prob_dist[indent]) \
                                  for indent in indents[0:4]])

    # likely dialog indents
    # most probable indent = indents[0]
    dial_indents = [indent for indent in indents if \
                    abs(indent -indents[0])<=3 and\
                    indent_prob_dist[indent]>=.01]

    ndial_indents = [indent for indent in indents \
                        if indent not in dial_indents]
    # likely narration indents
    narr_indents = [indent for indent in ndial_indents if \
                    abs(indent - ndial_indents[0])<=3 and\
                    # indents[0] - indent>=4 and\
                    indent_prob_dist[indent]>= .01]

    print("\tdialog indents=", dial_indents)
    print("\tnarration indents=", narr_indents)


    # case more narration than dialog
    if dial_indents and narr_indents:
        if max(dial_indents) < min(narr_indents):
            dial_indents, narr_indents = narr_indents, dial_indents

    # keep only narration and dialog indentations. Also remove smallest indent.
    new_lines = []
    for line in lines:
        indent = count_leading_wh_sp(line)
        if indent in dial_indents +  narr_indents:
            if len(narr_indents)==0:
                # there is no difference in indentation between narr and dial
                new_lines.append(line)
            else:
                if remove_dialog:
                    if indent in narr_indents:
                        new_lines.append(line[min(narr_indents):])
                else:
                    new_lines.append(line[min(narr_indents):])
    lines = new_lines

    # print("nnuu", lines[0:15])
    # print("nnuu", lines[-15:])

    # this didn't work
    # remove enumeration markers.
    # pattern = re.compile(r"^[^a-zA-Z]*")
    # lines = [re.sub(pattern, "", line) for line in lines]


    # join lines to create new script
    lines = [line.strip() for line in lines if line]
    script = ' '.join(lines)

    # split script into sentences
    lines = tokenize.sent_tokenize(script)

    with open(outpath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

def preprocess_batch_of_m_scripts(
        in_dir, out_dir,
        file_names,
        remove_dialog=False):

    all_file_names = os.listdir(in_dir)
    assert set(file_names) in set(all_file_names)
    for file_name in file_names:
        i = all_file_names.index(file_name)
        print('%i.' % (i + 1))
        preprocess_one_m_script(in_dir,
                                out_dir,
                                file_name,
                                remove_dialog=remove_dialog)

if __name__ == "__main__":
    from my_globals import *
    def main1():
        remove_dialog = True
        in_dir = M_SCRIPTS_DIR
        if remove_dialog:
            out_dir = PREP_DIR
        else:
            out_dir = PREP_RD_DIR
        file_names = os.listdir(in_dir)[0:2]
        preprocess_batch_of_m_scripts(
            in_dir, out_dir,
            file_names,
            remove_dialog=remove_dialog)

        file_name = "x-men.txt"
        preprocess_one_m_script(in_dir,
                                out_dir,
                                file_name,
                                remove_dialog=remove_dialog)
    def main2():
        remove_dialog = False
        in_dir = "short_stories"
        out_dir = "short_stories_prep"
        file_names = os.listdir(in_dir)[0:2]
        preprocess_batch_of_m_scripts(
            in_dir, out_dir,
            file_names,
            remove_dialog=remove_dialog)

    # main1()
    main2()