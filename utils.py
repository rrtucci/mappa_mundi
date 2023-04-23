import os
from my_globals import *
import shutil

def zero_based_position_from_m_title(title):
    return my_listdir(M_SCRIPTS_DIR).index(title + ".txt")

def m_title_from_zero_based_position(pos):
    return my_listdir(M_SCRIPTS_DIR)[pos][:-len(".txt")]

def argmax_of_list(l):
    return max(range(len(l)), key=(lambda i: l[i]))

def print_welcome_message():
    print("Welcome Causal AI Navigator. We have been waiting for you for "
          "millenia. Where would you like us to go next?")

def my_listdir(dir):
    # listdir includes hidden files like .ipynb_checkpoints
    checkpoints = dir + "/" +  ".ipynb_checkpoints"
    shutil.rmtree(checkpoints, ignore_errors=True)
    return os.listdir(dir)




