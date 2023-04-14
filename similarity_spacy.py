from itertools import product
import numpy as np
import spacy
nlp = spacy.load('en_core_web_lg')


def ztz_similarity(ztz1, ztz2):
    def same_pos(token1, token2):
        return token1.pos_ == token2.pos_
        # return True

    special_pos = ['NOUN', 'ADJ', 'ADV', 'VERB']
    doc1 = nlp(ztz1)
    doc2 = nlp(ztz2)
    sp_tokens1 = [token1 for token1 in doc1 \
                    if token1.pos_ in special_pos]
    sp_tokens2 = [token2 for token2 in doc2 \
                    if token2.pos_ in special_pos]
    token_pair_to_simi = {}
    for token1, token2 in product(sp_tokens1, sp_tokens2):
        if same_pos(token1, token2):
            simi = nlp(token1.text.lower()).\
                similarity(nlp(token2.text.lower()))
            # print("llkj", token1.text, token2.text, token1.pos_, simi)
            if simi is not None:
                token_pair_to_simi[(token1, token2)]= simi
    # print("ffgh", "****************")
    # ("mmnk", token_pair_to_simi)
    score1 = 0.0
    count1 = 0
    for token1 in sp_tokens1:
        simi_list = [token_pair_to_simi[(token1, token2)]
                for token2 in sp_tokens2
                if same_pos(token1, token2)]
        if simi_list:
            best_score = max(simi_list)
            score1 += best_score
            count1 += 1
    if count1:
        score1 /= count1

    score2 = 0.0
    count2 = 0
    for token2 in sp_tokens2:
        simi_list =[token_pair_to_simi[(token1, token2)]
                          for token1 in sp_tokens1
                   if same_pos(token1, token2)]
        if simi_list:
            best_score = max(simi_list)
            score2 += best_score
            count2 += 1
    if count2:
        score2 /= count2
    prob = (score1 + score2) / 2
    if prob<1:
        odds = prob/ (1 - prob)
    else:
        odds = 10e6
    return round(odds ,3)

SIMI_THRESHOLD = 2.69

# ************ simi definition from: similarity_spacy
# 1. Cats are beautiful animals.
# 2. Dogs are awesome.
# simi(1,2)= 2.578
#
# 1. Dogs are awesome.
# 2. Cats are beautiful animals.
# simi(1,2)= 2.578
#
# 1. Cats are beautiful animals.
# 2. Some gorgeous creatures are felines.
# simi(1,2)= 2.697
#
# 1. Some gorgeous creatures are felines.
# 2. Cats are beautiful animals.
# simi(1,2)= 2.697
#
# 1. Cats are beautiful animals.
# 2. Dolphins are swimming mammals.
# simi(1,2)= 2.535
#
# 1. Dolphins are swimming mammals.
# 2. Cats are beautiful animals.
# simi(1,2)= 2.535
#
# 1. Cats are beautiful animals.
# 2. Cats are beautiful animals.
# simi(1,2)= 10000000.0
#
# 1. Cats are beautiful animals.
# 2. Cats are beautiful animals.
# simi(1,2)= 10000000.0
#
# ************ simi definition from: similarity_spacy
# apple-horse, horse-apple 0.247 0.247
# Paul-John 0.0
#
# 1. The cat sat on the mat.
# 2. The dog lay on the rug.
# simi(1, 2)= 1.678
# elapsed time= 0.08501148223876953