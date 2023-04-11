import os
from my_globals import *

def zero_based_position_from_m_title(title):
    return os.listdir(M_SCRIPTS_DIR).index(title + ".txt")

def m_title_from_zero_based_position(pos):
    return os.listdir(M_SCRIPTS_DIR)[pos][:-len(".tex")]


