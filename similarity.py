"""

This file has functions to test the function `ztz_similarity(str1, str2)`
which measures the similarity of two sentences `ztz1` and `ztz2`.
`ztz_similarity()` has been implemented 4 different ways, in separate files

1. similarity_bert.py (Recommended)
Uses BERT and sentence-transformers

2. similarity_nltk.py
Uses NLTK + WordNet

3. similarity_spacy.py
Uses SpaCy + WordVec

4. similarity_spacy2.py
Attempt to use SpaCy + WordNet

"""
from my_globals import *
import importlib as imp
from sentence_transformers import SentenceTransformer

simi_def = imp.import_module(SIMI_DEF)


def print_simi_12(str1, str2, **kwargs):
    """
    Prints similarity of `str1` and `str2`.

    Parameters
    ----------
    str1: str
    str2: str

    Returns
    -------
    None

    """
    print()
    print("1.", str1)
    print("2.", str2)
    simi12 = simi_def.ztz_similarity(str1, str2, **kwargs)
    simi21 = simi_def.ztz_similarity(str2, str1, **kwargs)
    print("simi(1, 2)=", str(simi12))
    print("simi(2, 1)=", str(simi21))


if __name__ == "__main__":
    def main1():
        if SIMI_DEF == "similarity_bert":
            model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            model = None
        print("************ simi definition from:", SIMI_DEF)

        ztzs = [
            "Dogs are awesome.",
            "Some gorgeous creatures are felines.",
            "Dolphins are swimming mammals.",
            "Cats are beautiful animals.",
            "Cats are beauti animals.",
        ]

        focus_ztz = "Cats are beautiful animals."
        for ztz in ztzs:
            print_simi_12(focus_ztz, ztz, model=model)


    def main2():
        if SIMI_DEF == "similarity_bert":
            model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            model = None
        print("************ simi definition from:", SIMI_DEF)
        word1, word2 = "apple", "horse"
        print_simi_12(word1, word2, model=model)
        print_simi_12("Paul", "John", model=model)

        ztz1 = "The cat sat on the mat."
        ztz2 = "The dog lay on the rug."
        print_simi_12(ztz1, ztz2, model=model)


    main1()
    main2()
