"""
https://spacy.io/usage/spacy-101/

For spacy, token.dep_ dictionary

cc: coordinating conjunction.
    i.e., FANBOYS = for, and, nor, but, or, yet, so

mark: marker that introduces a subordinate clause

ADP: adposition, e.g. in, to, during

"""

import spacy
import re
from my_globals import *

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("merge_entities")


def simplify_ztz(sentence, verbose=False):
    doc = nlp(sentence)
    tokenized_clauses_list = []
    tokenized_clause = []
    for token in doc:
        cond = (token.dep_ == "mark") or \
                (token.dep_ == "cc") or \
                (token.text==";")
        if not cond:
            tokenized_clause.append(token)
        else:
            tokenized_clauses_list.append(tokenized_clause)
            tokenized_clause = []
    # last clause
    tokenized_clauses_list.append(tokenized_clause)


    ztz_list = []
    for tokenized_clause in tokenized_clauses_list:

        # replace by empty list any tokenized clause
        # that doesn't have a noun/pronoun and a verb
        clause_has_noun_or_pronoun = False
        clause_has_verb = False
        for token in tokenized_clause:
            if token.pos_ in ["NOUN", "PRON", "PROPN"]:
                clause_has_noun_or_pronoun = True
                # print("NOUN or PRONOUN", token.text)
            if token.pos_ in ["VERB", "AUX"]:
                clause_has_verb = True
                # print("VERB", token.text)
        if not (clause_has_noun_or_pronoun and clause_has_verb):
            tokenized_clause = []

        str_list = []
        for token in tokenized_clause:
            x = token.text
            if token.ent_type_:
                # replace named entities by their labels
                # x = token.ent_type_
                # remove named entities
                x = ""
            if token.is_stop and (token.pos_ not in RETAINED_STOPWORD_POS):
                x =""
            if token.pos_ not in RETAINED_POS:
                # remove stop words, except RETAINED_POS
                x =""
            str_list.append(x)
        #print("mxml", str_list)
        ztz = " ".join(str_list)
        # remove all remaining punctuation marks
        ztz = re.sub(r'[^\w\s]', '', ztz).strip()
        # if ztz is just one word, replace it by ""
        if ztz.isalpha():
            ztz = ''
        ztz_list.append(ztz)
    if verbose:
        print(sentence.strip())
        print(ztz_list)
    return ztz_list
