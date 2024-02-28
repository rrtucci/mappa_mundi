"""

This file holds some general purpose functions (utilities).

"""
import os
from globals import *
import shutil


def zero_based_position_from_m_title(dir_, title):
    """
    This method returns the position (zero based, starting from zero) of
    title `title` in directory `dir_`.

    Parameters
    ----------
    dir_: str
    title: str

    Returns
    -------
    int

    """
    return list(my_listdir(dir_)).index(title + ".txt")


def m_title_from_zero_based_position(dir_, pos):
    """
    This method returns the title in directory `dir_` of the movie at
    position `pos` (zero based, starting from zero).

    Parameters
    ----------
    dir_: str
    pos: int

    Returns
    -------
    str

    """
    return list(my_listdir(dir_))[pos][:-len(".txt")]


def argmax_of_list(lista):
    """
    This method returns the argmax of list `lista`.

    Parameters
    ----------
    lista: list[X]

    Returns
    -------
    type(X)


    """
    return max(range(len(lista)), key=(lambda i: lista[i]))


def print_welcome_message():
    """
    This method prints a welcome message.

    Returns
    -------
    None

    """
    print("Welcome Causal AI Navigator. We have been waiting for you for "
          "millennia. Where would you like us to go next?")


def my_listdir(dir_):
    """
    Whenever one opens a text file within directory `dir_` using jupyter lab
    ( JL), JL writes an annoying `.ipynb.checkpoints` folder inside `dir_`.
    This method deletes that checkpoints folder and then returns the usual
    `os.listdir( dir_)`

    Parameters
    ----------
    dir_: str

    Returns
    -------
    iterable

    """
    # listdir includes hidden files like .ipynb_checkpoints
    checkpoints = dir_ + "/" + ".ipynb_checkpoints"
    shutil.rmtree(checkpoints, ignore_errors=True)
    # os.listdir list in arbitrary order!
    return sorted(os.listdir(dir_))


def get_prob_acc_and_nsam(num_acc, num_rej, round_digits=2):
    """
    This method returns the probability of acceptance `prob_acc` and the
    number of samples `nsam` used to calculate that probability.

    Parameters
    ----------
    num_acc: int
        number of times an arrow has been accepted
    num_rej: int
        number of times an arrow has been rejected.
    round_digits: int

    Returns
    -------
    float, int

    """
    nsam = num_acc + num_rej
    return round(num_acc / nsam, round_digits), nsam
