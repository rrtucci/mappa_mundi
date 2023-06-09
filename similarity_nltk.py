"""

This file contains a function `ztz_similarity(ztz1, ztz2)`
that returns the similarity of sentences `ztz1` and `ztz2`.
ztz = sentence

It uses NLTK + WordNet

Ref:
https://nlpforhackers.io/wordnet-sentence-similarity/

"""

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from itertools import product
from collections import defaultdict
from time import time


def penn_to_wn(tag):
    """
    Convert a Penn Treebank tag to a simplified Wordnet tag

    Parameters
    ----------
    tag: str

    Returns
    -------
    str

    """
    if tag.startswith('N'):
        return 'n'  # noun

    if tag.startswith('V'):
        return 'v'  # verb

    if tag.startswith('J'):
        return 'a'  # adjective

    if tag.startswith('R'):
        return 'r'  # adverb

    return None


def synset_for_tgd_word(tgd_word):
    """
    This private method returns the most likely synset for a tagged word
    `tgd_word`. A synset (synonym set) is a sort of equivalence class of
    words with very similar meanings.

    Parameters
    ----------
    tgd_word: tuple(str, str)

    Returns
    -------
    wn.synset or None

    """
    word, tag = tgd_word
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def ztz_similarity(ztz1, ztz2, **kwargs):
    """
    This method returns the similarity between sentences `ztz1` and `ztz2`.
    The similarity is measured as odds of a probability, so it ranges from 0
    to infinity.

    Parameters
    ----------
    ztz1: str
    ztz2: str

    Returns
    -------
    float

    """

    do_time = False
    if do_time:
        print("similarity start", time())
    # Tokenize and tag
    tgd_ztz1 = pos_tag(word_tokenize(ztz1.lower()))
    tgd_ztz2 = pos_tag(word_tokenize(ztz2.lower()))

    # Get the synsets for the tagged words (tgd_word)
    all_ss1 = []
    for tgd_word in tgd_ztz1:
        ss1 = synset_for_tgd_word(tgd_word)
        if ss1:
            all_ss1.append(ss1)
    all_ss2 = []
    for tgd_word in tgd_ztz2:
        ss2 = synset_for_tgd_word(tgd_word)
        if ss2:
            all_ss2.append(ss2)

    ss_pair_to_simi = defaultdict(lambda: 0)
    if do_time:
        print("similarity begin path_similarity()", time())
    for ss1, ss2 in product(all_ss1, all_ss2):
        simi = ss1.path_similarity(ss2)
        if simi is not None:
            ss_pair_to_simi[(ss1, ss2)] = simi

    score1 = 0.0
    count1 = 0
    for ss1 in all_ss1:
        simi_list = [ss_pair_to_simi[(ss1, ss2)] for ss2 in all_ss2]
        if simi_list:
            best_score = max(simi_list)
            score1 += best_score
            count1 += 1
    if count1:
        score1 /= count1

    score2 = 0.0
    count2 = 0
    for ss2 in all_ss2:
        simi_list = [ss_pair_to_simi[(ss1, ss2)] for ss1 in all_ss1]
        if simi_list:
            best_score = max(simi_list)
            score2 += best_score
            count2 += 1
    if count2:
        score2 /= count2
    prob = (score1 + score2) / 2
    if prob < 1:
        odds = prob / (1 - prob)
    else:
        odds = 1000
    if do_time:
        print("similarity ends", time())
    return round(odds, 3)


"""
************ simi definition from: similarity_nltk
1. Cats are beautiful animals.
2. Dogs are awesome.
simi(1, 2)= 1.045
simi(2, 1)= 1.045

1. Cats are beautiful animals.
2. Some gorgeous creatures are felines.
simi(1, 2)= 2.429
simi(2, 1)= 2.429

1. Cats are beautiful animals.
2. Dolphins are swimming mammals.
simi(1, 2)= 0.733
simi(2, 1)= 0.733

1. Cats are beautiful animals.
2. Cats are beautiful animals.
simi(1, 2)= 1000
simi(2, 1)= 1000

************ simi definition from: similarity_nltk
1. apple
2. horse
simi(1, 2)= 0.056
simi(2, 1)= 0.056

1. Paul
2. John
simi(1, 2)= 0.083
simi(2, 1)= 0.083

1. The cat sat on the mat.
2. The dog lay on the rug.
simi(1, 2)= 0.353
simi(2, 1)= 0.353
elapsed time= 0.006499767303466797

"""
