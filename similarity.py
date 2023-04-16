from my_globals import *
import importlib as imp
simi = imp.import_module(SIMI_DEF)
from time import time

def print_simi_12(str1, str2, timeit=False):
    print("1.", str1)
    print("2.", str2)
    if timeit:
        start = time()
        simi12 = simi.ztz_similarity(str1, str2)
        simi21 = simi.ztz_similarity(str2, str1)
        end = time()
    else:
        simi12 = simi.ztz_similarity(str1, str2)
        simi21 = simi.ztz_similarity(str2, str1)
    print("simi(1, 2)=", str(simi12))
    print("simi(2, 1)=", str(simi21))
    if timeit:
        print("elapsed time=", str((end-start)/2))
    print()


if __name__ == "__main__":
    def main1():
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
            print_simi_12(focus_ztz, ztz)

    def main2():
        print("************ simi definition from:", SIMI_DEF)
        word1, word2 = "apple", "horse"
        print_simi_12(word1, word2)
        print_simi_12("Paul", "John")

        ztz1 = "The cat sat on the mat."
        ztz2 = "The dog lay on the rug."
        print_simi_12(ztz1, ztz2, timeit=True)

    main1()
    main2()