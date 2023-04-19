"""
https://nlpforhackers.io/wordnet-sentence-similarity/

ztz = sentence
"""

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from itertools import product

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n' # noun

    if tag.startswith('V'):
        return 'v' # verb

    if tag.startswith('J'):
        return 'a' # adjective

    if tag.startswith('R'):
        return 'r' # adverb

    return None


def tword_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def ztz_similarity(ztz1, ztz2):
    """ compute the ztz similarity using Wordnet """
    # Tokenize and tag
    ztz1 = pos_tag(word_tokenize(ztz1.lower()))
    ztz2 = pos_tag(word_tokenize(ztz2.lower()))

    # Get the synsets for the tagged words (tword)
    all_ss1 = []
    for tword in ztz1:
        ss1 = tword_to_synset(*tword)
        if ss1:
            all_ss1.append(ss1)
    all_ss2 = []
    for tword in ztz2:
        ss2 = tword_to_synset(*tword)
        if ss2:
            all_ss2.append(ss2)

    ss_pair_to_simi = {}
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
    prob = (score1 + score2)/2
    if prob<1:
        odds = prob/ (1 - prob)
    else:
        odds = 1000
    return round(odds ,3)

SIMI_THRESHOLD = 2.2

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