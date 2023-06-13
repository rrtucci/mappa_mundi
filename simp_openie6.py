"""

This file contains one of several implementations of the function 
`simplify_ztz(sentence, verbose=False)` that we considered.

It is called within a jupyter notebook at Google colab 
https://colab.research.google.com/drive/1LdvsBPfYyREYofvZ4fX9LLW5njKSbQgy?usp=drive_link

The notebook was authored by Anton Alekseev and Anastasia Predelina. It 
installs the software for Openie6 (Ref.3)

Refs:

1. https://github.com/dair-iitd/CaRB

2. https://github.com/dair-iitd/imojie

3. https://github.com/dair-iitd/openie6

"""
import subprocess
from my_globals import *

def simplify_ztz(sentence, verbose=False, **kwargs):
    """
    This method simplifies the sentence `sentence`. It returns a list of
    simple sentences extracted from the input sentence.

    Parameters
    ----------
    sentence: str
    verbose: bool
    kwargs: dict[]

    Returns
    -------
    list[str]

    """

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
    # ztz_list has full sentence in first row
    return ztz_list[1:]
