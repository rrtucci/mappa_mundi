import spacy
import nltk
from nltk.corpus import wordnet as wn
from my_globals import *
from itertools import product
from collections import defaultdict
from time import time
nlp = spacy.load("en_core_web_sm")

def ztz_similarity(ztz1, ztz2):
    do_time = False
    if do_time:
        print("similarity begins", time())
    doc1 = nlp(ztz1)
    doc2 = nlp(ztz2)
    sp_tokens1 = [token1 for token1 in doc1 \
                  if token1.pos_ in RETAINED_POS]
    sp_tokens2 = [token2 for token2 in doc2 \
                  if token2.pos_ in RETAINED_POS] 
    all_ss1 = []
    for token1 in sp_tokens1:
        if wn.synsets(token1.text):
            ss1 = wn.synsets(token1.text)[0]
            all_ss1.append(ss1)
            
    all_ss2 = []
    for token2 in sp_tokens2:
        if wn.synsets(token2.text):
            ss2 = wn.synsets(token2.text)[0]
            all_ss2.append(ss2)
    ss_pair_to_simi = defaultdict(lambda: 0)
    if do_time:
        print("beginning of path_similarity()", time())
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
    if do_time:
        print("similarity ends", time())
    return round(odds ,3)

    
