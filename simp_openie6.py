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
    # live side by side inside a bigger folder
    # and that the cwd is `mappa_mundi`
    with open("../openie6_sentences.txt", "w") as f:
        f.write(sentence)

    gpu_command = \
        "cd ../openie6 && CUDA_DEVICE_ORDER=PCI_BUS_ID " \
        "CUDA_VISIBLE_DEVICES=0 " \
        "PYTHONPATH=imojie:imojie/allennlp:imojie" \
        "/pytorch_transformers:$PYTHONPATH python run.py " \
        "--save models/conj_model --mode predict " \
        "--inp ../openie6_sentences.txt --batch_size 1 " \
        "--model_str bert-large-cased --task conj " \
        "--gpus 1 --out ../openie6_predictions.txt"

    cpu_command = gpu_command.replace("--gpus 1", "--gpus 0")

    if USE_GPU:
        subprocess.Popen(gpu_command, shell=True)
    else:
        subprocess.Popen(cpu_command, shell=True)

    ztz_list = []
    with open("../openie6_predictions.txt.conj", "r") as f:
        for line in f:
            ztz_list.append(line)
    # ztz_list has original sentence in first row
    return ztz_list[1:]
