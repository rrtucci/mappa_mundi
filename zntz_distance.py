"""
https://nlpforhackers.io/wordnet-sentence-similarity/

zntz = sentence
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


def ztnz_similarity(ztnz1, ztnz2):
    """ compute the ztnz similarity using Wordnet """
    # Tokenize and tag
    ztnz1 = pos_tag(word_tokenize(ztnz1))
    ztnz2 = pos_tag(word_tokenize(ztnz2))

    # Get the synsets for the tagged words (tword)
    all_ss1 = []
    for tword in ztnz1:
        ss1 = tword_to_synset(*tword)
        if ss1:
            all_ss1.append(ss1)
    all_ss2 = []
    for tword in ztnz2:
        ss2 = tword_to_synset(*tword)
        if ss2:
            all_ss2.append(ss2)

    ss_pair_to_simi = {}
    for ss1, ss2 in product(all_ss1, all_ss2):
        simi = ss1.path_similarity(ss2)
        if simi:
            ss_pair_to_simi[(ss1, ss2)] = simi

    score1 = 0.0
    count1 = 0
    for ss1 in all_ss1:
        best_score = max([ss_pair_to_simi[(ss1, ss2)] for ss2 in all_ss2])
        if best_score is not None:
            score1 += best_score
            count1 += 1
    score1 /= count1

    score2 = 0.0
    count2 = 0
    for ss2 in all_ss2:
        best_score = max([ss_pair_to_simi[(ss1, ss2)] for ss1 in all_ss1])
        if best_score is not None:
            score2 += best_score
            count2 += 1
    score2 /= count2
    return round((score1 + score2)/2, 3)


if __name__ == "__main__":
    def main1():

        ztnzs = [
            "Dogs are awesome.",
            "Some gorgeous creatures are felines.",
            "Dolphins are swimming mammals.",
            "Cats are beautiful animals.",
        ]

        focus_ztnz = "Cats are beautiful animals."

        for ztnz in ztnzs:
            print("Similarity(\"%s\", \"%s\") = %s" % (
            focus_ztnz, ztnz,
            ztnz_similarity(focus_ztnz, ztnz)))
            print(
            "Similarity(\"%s\", \"%s\") = %s" % (
            ztnz, focus_ztnz,
            ztnz_similarity(ztnz, focus_ztnz)))

    def main2():
        print("apple-horse, horse-apple",
              ztnz_similarity("apple", "horse"),
              ztnz_similarity("horse", "apple"))

        ztnz1 = "The cat sat on the mat."
        ztnz2 = "The dog lay on the rug."
        similarity = ztnz_similarity(ztnz1, ztnz2)
        print("Similarity between 2 ztnzs: ", similarity)

    main1()
    main2()
