"""

This file holds some general purpose functions (utilities).

"""
import os
from my_globals import *
import shutil


def zero_based_position_from_m_title(dir, title):
    """
    This method returns the position (zero based, starting from zero) of
    title `title` in directory `dir`.

    Parameters
    ----------
    dir: str
    title: str

    Returns
    -------
    int

    """
    return list(my_listdir(dir)).index(title + ".txt")


def m_title_from_zero_based_position(dir, pos):
    """
    This method returns the title in directory `dir` of the movie at
    position `pos` (zero based, starting from zero).

    Parameters
    ----------
    pos: int

    Returns
    -------
    str

    """
    return list(my_listdir(dir))[pos][:-len(".txt")]


def argmax_of_list(l):
    """
    This method returns the argmax of list `l`.

    Parameters
    ----------
    l: list[X]

    Returns
    -------
    type(X)


    """
    return max(range(len(l)), key=(lambda i: l[i]))


def print_welcome_message():
    """
    This method prints a welcome message.

    Returns
    -------
    None

    """
    print("Welcome Causal AI Navigator. We have been waiting for you for "
          "millenia. Where would you like us to go next?")


def my_listdir(dir):
    """
    Whenever one opens a text file within directory `dir` using jupyter lab
    ( JL), JL writes an annoying `.ipynb.checkpoints` folder inside `dir`.
    This method deletes that checkpoints folder and then returns the usual
    `os.listdir( dir)`

    Parameters
    ----------
    dir: str

    Returns
    -------
    iterable

    """
    # listdir includes hidden files like .ipynb_checkpoints
    checkpoints = dir + "/" + ".ipynb_checkpoints"
    shutil.rmtree(checkpoints, ignore_errors=True)
    return os.listdir(dir)
