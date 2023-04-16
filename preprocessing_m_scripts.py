"""
https://www.datacamp.com/tutorial/python-regular-expression-tutorial

"""
import re
import os
# sentence splitting with NLKT
# from nltk.tokenize import sent_tokenize
import collections as co
from my_globals import *
import contractions
from unidecode import unidecode

# sentence splitting with spacy
import spacy
nlp = spacy.load('en_core_web_sm')


def preprocess_one_m_script(in_dir,
                            out_dir,
                            file_name,
                            remove_dialog=False):
    """
    in_dir and out_dir can be the same, but this will overwrite the files
    """
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
    pattern_paren = re.compile(r'\[(.*?)\]|\((.*?)\)|\{(.*?)\}')
    # regex for period followed by white spaces + number
    pattern_period = r"\.(?=\s*\d)"

    # Substitutions. If this results in empty line,
    # remove it.
    new_lines = []
    for line in lines:
        # print("ssdf", line)
        # remove parenthetical remarks
        line = re.sub(pattern_paren, "", line)
        # Replace tabs by 12 blank spaces
        line = re.sub(r"\t", " "*12, line)
        # replace period by dash if period followed by number
        line = re.sub(pattern_period, "-", line)
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
    # Found cases where line was just "is."
    pattern_lc = re.compile(r'^(.*[a-z]){2,}.*$')

    # Reject lines that don't contain at least 2 lower case letters string.
    # This gets rid of scene directions and character invocations.
    lines = [line for line in lines if re.search(pattern_lc, line)]

    white_spaces = [count_leading_wh_sp(line) for line in lines]
    # Counter returns dictionary mapping item to its number of repetitions
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

    # keep only narration (less likely than narration) indentations. Also
    # remove smallest indent.
    new_lines = []
    for line in lines:
        indent = count_leading_wh_sp(line)
        if indent in dial_indents +  narr_indents:
            if not narr_indents or not dial_indents:
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

    # Remove contractions and replace curly quotes by straight ones
    expanded_words = []
    for word in script.split():
        word = unidecode(word)
        expanded_words.append(contractions.fix(word))
    script = ' '.join(expanded_words)

    # split script into sentences

    # with NLKT
    # lines = sent_tokenize(script)

    # with spacy
    lines = nlp(script).sents
    # for line in lines:
    #     print("zzzxc", line)

    # remove sentences that are a single character
    lines = [line.text for line in lines if len(line.text)>1]

    with open(outpath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

def preprocess_batch_of_m_scripts(
        in_dir, out_dir,
        batch_file_names,
        remove_dialog=False):

    all_file_names = os.listdir(in_dir)
    assert set(batch_file_names).issubset(set(all_file_names))
    for file_name in batch_file_names:
        i = all_file_names.index(file_name)
        print('%i.' % (i + 1))
        preprocess_one_m_script(in_dir,
                                out_dir,
                                file_name,
                                remove_dialog=remove_dialog)


if __name__ == "__main__":
    from my_globals import *
    def main1():
        remove_dialog = False
        in_dir = "short_stories"
        out_dir = "short_stories_prep"
        batch_file_names = os.listdir(in_dir)[0:2]
        preprocess_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names,
            remove_dialog=remove_dialog)

    def main2():
        remove_dialog = True
        preprocess_one_m_script(
            in_dir=M_SCRIPTS_DIR,
            out_dir=PREP_DIR if not remove_dialog else PREP_RD_DIR,
            file_name = "x-men.txt",
            remove_dialog=remove_dialog)

    def main3():
        remove_dialog = False
        preprocess_batch_of_m_scripts(
            in_dir=M_SCRIPTS_DIR,
            out_dir=PREP_DIR if not remove_dialog else PREP_RD_DIR,
            batch_file_names=os.listdir(M_SCRIPTS_DIR)[0:10],
            remove_dialog=remove_dialog)

    main1()
    # main2()
    # main3()