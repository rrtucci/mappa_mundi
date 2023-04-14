from my_globals import *
import importlib as imp
simi = imp.import_module(SIMI_DEF)
from time import time

if __name__ == "__main__":
    def main1():
        print("************ simi definition from:", SIMI_DEF)

        ztzs = [
            "Dogs are awesome.",
            "Some gorgeous creatures are felines.",
            "Dolphins are swimming mammals.",
            "Cats are beautiful animals.",
        ]

        focus_ztz = "Cats are beautiful animals."


        for ztz in ztzs:
            print("1.", focus_ztz)
            print("2.", ztz)
            print("simi(1,2)=", simi.ztz_similarity(focus_ztz, ztz))
            print()
            print("1.", ztz)
            print("2.", focus_ztz)
            print("simi(1,2)=", simi.ztz_similarity(ztz, focus_ztz))
            print()

    def main2():
        print("************ simi definition from:", SIMI_DEF)
        print("apple-horse, horse-apple",
              simi.ztz_similarity("apple", "horse"),
              simi.ztz_similarity("horse", "apple"))
        print("Paul-John", simi.ztz_similarity("Paul", "John"))

        ztz1 = "The cat sat on the mat."
        ztz2 = "The dog lay on the rug."

        print()
        print("1.", ztz1)
        print("2.", ztz2)
        start = time()
        similarity = simi.ztz_similarity(ztz1, ztz2)
        end = time()
        elapsed_time = end -start
        print("simi(1, 2)=", str(similarity))
        print("elapsed time=", str(elapsed_time))

    main1()
    main2()