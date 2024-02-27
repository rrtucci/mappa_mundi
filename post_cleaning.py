"""

This file contains functions for post-cleaning movie scripts (or short
stories).

input directory: m_scripts_simp or short_stories_simp
output directory: m_scripts_post_clean or short_stories_post_clean

The input files have one or more sublines per line. For each file, we use
post clean the sublines by removing stop-words, punctuation marks, proper
nouns (a.k.a. named entities) and other excess baggage. Then we replace each
subline by its post-clean version. Different clean sublines from the
same sentence are put in the same line, separated by ZTZ_SEPARATOR . Some
sentences are diminished to nothing after the post-cleaning. Those
sentences are replaced by a single ZTZ_SEPARATOR.


Refs:
https://spacy.io/usage/spacy-101/

For spacy, here are some values of token.dep_

cc: coordinating conjunction.
    i.e., FANBOYS = for, and, nor, but, or, yet, so

mark: marker that introduces a subordinate subline

ADP: adposition, e.g. in, to, during

"""
from globals import *
import importlib as imp

zsimp = imp.import_module(ZTZ_SIMPLIFIER)
from utils import *

import spacy
import re
from globals import *

nlp = spacy.load("en_core_web_sm")


# nlp.add_pipe("merge_entities")


def post_clean_line(line, verbose=False):
    """
    This method cleans the line string `line`. It returns a list of simple
    sentences (sublines) extracted from the input sentence (line).

    Parameters
    ----------
    line: str
    verbose: bool

    Returns
    -------
    list[str]

    """
    tokenized_sublines = \
        [nlp(subline) for subline in line.split(ZTZ_SEPARATOR)]

    ztz_list = []
    for tokenized_subline in tokenized_sublines:

        # replace by empty list any tokenized subline
        # that doesn't have a noun/pronoun and a verb
        subline_has_noun_or_pronoun = False
        subline_has_verb = False
        token_str_list = []
        for token in tokenized_subline:
            x = get_post_cleaned_token_txt(token)
            if x:
                token_str_list.append(x)
            if token.pos_ in ["NOUN", "PRON", "PROPN"] and x:
                subline_has_noun_or_pronoun = True
                # print("NOUN or PRONOUN", token.text)
            if token.pos_ in ["VERB", "AUX"] and x:
                subline_has_verb = True
                # print("VERB", token.text)
        if not (subline_has_noun_or_pronoun and subline_has_verb):
            subline_str = []
        else:
            subline_str = " ".join(token_str_list)

        if subline_str:
            ztz_list.append(subline_str)

    if verbose:
        print(line.strip())
        print(ztz_list)
    return ztz_list


def get_post_cleaned_token_txt(token):
    """
    This auxiliary method takes as input a SpaCy Token `token` and returns a
    simplified version of the token's text.

    Parameters
    ----------
    token: Token

    Returns
    -------
    str

    """
    x = token.text
    # remove all punctuation marks
    x = re.sub(r'[^\w\s]', '', x)

    # if token.ent_type_:
    #     # replace named entities by their labels
    #     # x = token.ent_type_
    #
    #     # remove named entities
    #     x = ""
    # if token.is_stop and (token.pos_ not in RETAINED_STOPWORD_POS):
    #     x = ""
    # if token.pos_ not in RETAINED_POS:
    #     x = ""

    # remove single character tokens
    if len(x.strip()) == 1:
        x = ""
    x = x.strip()
    return x


def post_clean_one_m_script(
        in_dir, out_dir,
        file_name,
        verbose=False):
    """
    in_dir and out_dir can be the same, but this will overwrite the files.

    This method reads a file called `file_name` in the `in_dir` directory
    and creates a post-cleaned version in the `out_dir` directory.


    Parameters
    ----------
    in_dir: str
    out_dir: str
    file_name: str
    verbose: bool

    Returns
    -------
    None

    """
    inpath = in_dir + "/" + file_name
    outpath = out_dir + "/" + file_name
    new_lines = []
    with open(inpath, "r") as f:
        count = 1
        for line in f:
            if verbose:
                print(str(count) + ".")
            simple_ztz_list = post_clean_line(line,
                                              verbose=verbose)

            # remove empty simple ztz
            simple_ztz_list = [ztz for ztz in simple_ztz_list if ztz]

            if not simple_ztz_list:
                simple_ztz_list = [ZTZ_SEPARATOR]

            # replace multiple white spaces by single white space
            simple_ztz_list = [re.sub(r'\s+', ' ', ztz) for ztz in
                               simple_ztz_list]

            if len(simple_ztz_list) > 1:
                xx = " " + ZTZ_SEPARATOR + " "
                new_lines.append(xx.join(simple_ztz_list))
            elif len(simple_ztz_list) == 1:
                new_lines.append(simple_ztz_list[0])
            else:
                assert False

            count += 1
    with open(outpath, "w") as f:
        for line in new_lines:
            f.write(line + "\n")


def post_clean_batch_of_m_scripts(
        in_dir, out_dir,
        batch_file_names,
        verbose=False):
    """
    This method calls the method `post_clean_one_m_script` for all the file
    names in the list of file names `batch_file_names`.


    Parameters
    ----------
    in_dir: str
    out_dir: str
    batch_file_names: list[str]
    verbose: bool

    Returns
    -------
    None

    """
    all_file_names = my_listdir(in_dir)
    assert set(batch_file_names).issubset(set(all_file_names))
    for file_name in batch_file_names:
        i = all_file_names.index(file_name)
        print('%i.' % (i + 1), file_name)
        post_clean_one_m_script(in_dir, out_dir, file_name, verbose)


if __name__ == "__main__":
    def main1():
        in_dir = "short_stories_simp"
        out_dir = "short_stories_post_clean"
        batch_file_names = my_listdir(in_dir)[0:3]
        post_clean_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names,
            verbose=False)


    def main2():
        remove_dialogs = False
        in_dir = SIMP_DIR if not remove_dialogs else SIMP_RD_DIR
        out_dir = POST_CLEAN_DIR if not remove_dialogs else POST_CLEAN_RD_DIR
        batch_file_names = my_listdir(in_dir)[0:3]
        post_clean_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names)

    main1()
    main2()
