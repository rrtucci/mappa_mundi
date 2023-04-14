from my_globals import *
import importlib as imp
simi = imp.import_module(SIMI_DEF)

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
            print("Similarity(\"%s\", \"%s\") = %s" % (
            focus_ztz, ztz,
            simi.ztz_similarity(focus_ztz, ztz)))
            print(
            "Similarity(\"%s\", \"%s\") = %s" % (
            ztz, focus_ztz,
            simi.ztz_similarity(ztz, focus_ztz)))

    def main2():
        print("************ simi definition from:", SIMI_DEF)
        print("apple-horse, horse-apple",
              simi.ztz_similarity("apple", "horse"),
              simi.ztz_similarity("horse", "apple"))
        print("Paul-John", simi.ztz_similarity("Paul", "John"))

        ztz1 = "The cat sat on the mat."
        ztz2 = "The dog lay on the rug."
        similarity = simi.ztz_similarity(ztz1, ztz2)
        print("Similarity between 2 ztzs: ", similarity)

    main1()
    main2()