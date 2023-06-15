"""

The functions in this file are used inside the following jupyter notebook at
Google Colab

https://colab.research.google.com/drive/1S2EWOGkoCgjfOJzTRJ7PLeu4T8SBwhlF?usp=sharing

Refs:

1. https://github.com/dair-iitd/CaRB

2. https://github.com/dair-iitd/imojie

3. https://github.com/dair-iitd/openie6

"""
import subprocess
import os
from my_globals import *


def openie6_simplify_batch_of_m_scripts(
        in_dir, out_dir,
        batch_file_names,
        verbose=False):
    """
    This method does the same thing as the method
    `simplifying.simplify_batch_of_m_scripts()` but for the case
    `ZTZ_SIMPLIFIER = "simp_openie6"`

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
    # assume directories `openie6` and `mappa_mundi`
    # live side by side inside a bigger folder X
    # and that the cwd X

    m_script_starting_line_nums = \
        make_all_sentences_file(in_dir='mappa_mundi' + "/" + in_dir,
                                batch_file_names=batch_file_names)
    gpu_command = \
        "cd openie6 && CUDA_DEVICE_ORDER=PCI_BUS_ID " \
        "CUDA_VISIBLE_DEVICES=0 " \
        "PYTHONPATH=imojie:imojie/allennlp:imojie" \
        "/pytorch_transformers:$PYTHONPATH python run.py " \
        "--save models/conj_model --mode predict " \
        "--inp ../all_sentences.txt --batch_size 1 " \
        "--model_str bert-large-cased --task conj " \
        "--gpus 1 --out ../all_predictions.txt"

    cpu_command = gpu_command.replace("--gpus 1", "--gpus 0")

    if USE_GPU:
        subprocess.Popen(gpu_command, shell=True)
    else:
        subprocess.Popen(cpu_command, shell=True)

    translate_predictions_file_from_openie6_to_mm(
        in_fname="all_predictions.txt.conj",
        out_fname="all_predictions_in_mm.txt")

    make_m_scripts_simp_dir(batch_file_names,
                            m_script_starting_line_nums)

    os.remove("all_sentences.txt")
    os.remove("all_predictions.txt")
    os.remove("all_predictions_in_mm.txt")


def make_all_sentences_file(in_dir, batch_file_names):
    """
    This internal method creates the file `all_sentences.txt`.
    `all_sentences.txt` is a concatenation of all the files in
    `batch_file_names`.

    Parameters
    ----------
    in_dir: str
    batch_file_names: list[str]

    Returns
    -------
    m_script_starting_line_nums: list[int]
        list of the starting line numbers within the file
        `all_sentences.txt` for the file names in the list `batch_file_names`.

    """
    m_script_starting_line_nums = []
    cum_line_num = 0
    with open("all_sentences.txt", "w") as big_f:
        for fname in batch_file_names:
            in_path = in_dir + '/' + fname
            with open(in_path, "r") as f:
                m_script_starting_line_nums.append(cum_line_num)
                f_len = sum(1 for _ in f)
                cum_line_num += f_len
                for line in f:
                    big_f.write(line)
    return m_script_starting_line_nums


def translate_predictions_file_from_openie6_to_mm(in_fname, out_fname):
    """
    This internal method reads the file `all_predictions.txt.conj` and
    translates it into a new file called `all_predictions_in_mm.txt`. The
    input file is in the format of openie6 extractions output and the output
    one is in the mappa mundi (mm) simp format.

    openie6 extractions output format: one sentence or empty space per line.
    Groups separated by empty line. Each group consists of the original
    sentence followed by the extraction sentences.

    mm simp format: one sentence per line. No empty lines. Each line has all
    the extractions from a single sentence, separated by ZTZ_SEPARATOR.

    Parameters
    ----------
    in_fname: str
    out_fname: str

    Returns
    -------
    None

    """
    with open(in_fname, "r") as in_file:
        with open(out_fname, "w") as out_file:
            in_parts = []
            original_ztz = True
            for line in in_file:
                if line:
                    if not original_ztz:
                        in_parts.append(line)
                else:
                    original_ztz = True
                    out_file.write(ZTZ_SEPARATOR.join(in_parts) + "\n")
                    in_parts = []


def make_m_scripts_simp_dir(batch_file_names,
                            m_script_starting_line_nums):
    """
    This internal method reads the file `all_predictions_in_mm.txt` and it
    uses that to create a new directory populated by files with the names of
    file names in list `batch_file_names'.

    Parameters
    ----------
    batch_file_names: list[str]
    m_script_starting_line_nums: list[int]

    Returns
    -------
    None

    """
    with open("all_sentences_in_mm.txt", "r") as big_f:
        m_script_num = -1
        for line_num, line in enumerate(big_f):
            if line_num in m_script_starting_line_nums:
                if f:
                    f.close()
                m_script_num += 1
                fname = batch_file_names[m_script_num]
                out_path = "m_scripts_simp" + "/" + fname
                f = open(out_path, "w")
            f.write(line)
        if f:
            f.close()