"""

This file contains functions for simplifying movie scripts (or short stories).

input directory: m_scripts_spell or short_stories_spell
output directory: m_scripts_simp or short_stories_simp

Simplification is done by the function `simplify_ztz()`. This function was
implemented in several ways before we decided to stick with the version in
file `simp_spacy3`.

simp_spacy1.py
simp_spacy2.py
simp_spacy3.py (recommended)
simp_spacy-claucy.py
simp_stanford.py

The input files have only one sentence per line. For each file, we use SpaCy
to break each sentence into clauses. Then we simplify the clauses by
removing stop-words, punctuation marks, proper nouns (a.k.a. named entities)
and other excess baggage. Then we replace each clause by its simplified
version. Different simplified clauses from the same sentence are put in the
same line, separated by a separator-token. Some sentences are diminished to
nothing after the simplification. Those sentences are replaced by a single
asterisk.

"""
from globals import *
import os
import re
import importlib as imp

zsimp = imp.import_module(ZTZ_SIMPLIFIER)
from utils import *


def simplify_one_m_script(
        in_dir, out_dir,
        file_name,
        verbose=False,
        use_gpu=False):
    """
    in_dir and out_dir can be the same, but this will overwrite the files.

    This method reads a file called `file_name` in the `in_dir` directory
    and creates a simplified version in the `out_dir` directory.


    Parameters
    ----------
    in_dir: str
    out_dir: str
    file_name: str
    verbose: bool
    use_gpu: bool

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
            simple_ztz_list = zsimp.simplify_ztz(line,
                                                 verbose=verbose,
                                                 use_gpu=use_gpu)

            # remove empty clauses
            simple_ztz_list = [ztz for ztz in simple_ztz_list if ztz]

            if simple_ztz_list == []:
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


def simplify_batch_of_m_scripts(
        in_dir, out_dir,
        batch_file_names,
        verbose=False):
    """
    This method calls the method `simplify_one_m_script` for all the file
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
        simplify_one_m_script(in_dir, out_dir, file_name, verbose)


if __name__ == "__main__":

    def main1():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        ztz = \
            'The man, who had never liked the words' \
            ' "booby" and "boobyhatch,"' \
            ' and who liked them even less on a shining morning when there' \
            ' was a unicorn in the garden, thought for a moment.'
        zsimp.simplify_ztz(ztz, verbose=True)


    def main2():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        path = "simplifying_test.txt"
        with open(path, "r") as f:
            count = 1
            for line in f:
                print(str(count) + ".")
                zsimp.simplify_ztz(line, verbose=True)
                count += 1


    def main3():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        in_dir = "short_stories_spell"
        out_dir = "short_stories_simp"
        batch_file_names = my_listdir(in_dir)[0:3]
        simplify_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names,
            verbose=False)


    def main4():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        remove_dialogs = False
        in_dir = SPELL_DIR if not remove_dialogs else SPELL_RD_DIR
        out_dir = SIMP_DIR if not remove_dialogs else SIMP_RD_DIR
        batch_file_names = my_listdir(in_dir)[0:3]
        simplify_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names)


    main1()
    main2()
    # main3()
    # main4()
