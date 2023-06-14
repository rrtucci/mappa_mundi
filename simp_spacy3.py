"""

This file contains one of several implementations of the function
`simplify_ztz(sentence, verbose=False)` that we considered.

Refs:
https://spacy.io/usage/spacy-101/

For spacy, here are some values of token.dep_

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
    """
    This method simplifies the sentence `sentence`. It returns a list of
    simple sentences extracted from the input sentence.

    Parameters
    ----------
    sentence: str
    verbose: bool
    kwargs: dict[]

    Returns
    -------
    list[str]

    """
    doc = nlp(sentence)
    tokenized_clauses_list = []
    tokenized_clause = []
    for token in doc:
        cond = (token.dep_ == "mark") or \
               (token.dep_ == "cc") or \
               (token.text == ";")
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
        token_str_list = []
        for token in tokenized_clause:
            x = get_simplified_token_txt(token)
            if x:
                token_str_list.append(x)
            if token.pos_ in ["NOUN", "PRON", "PROPN"] and x:
                clause_has_noun_or_pronoun = True
                # print("NOUN or PRONOUN", token.text)
            if token.pos_ in ["VERB", "AUX"] and x:
                clause_has_verb = True
                # print("VERB", token.text)
        if not (clause_has_noun_or_pronoun and clause_has_verb):
            clause_str = []
        else:
            clause_str = " ".join(token_str_list)

        if clause_str:
            ztz_list.append(clause_str)

    if verbose:
        print(sentence.strip())
        print(ztz_list)
    return ztz_list


def get_simplified_token_txt(token):
    """
    This auxiliary method takes as input a SpaCy Token `token` and returns a
    simplified version of the token's text.

    Parameters
    ----------
    token: Token

    Returns
    -------
    str

    """
    x = token.text
    # remove all punctuation marks
    x = re.sub(r'[^\w\s]', '', x)
    if token.ent_type_:
        # replace named entities by their labels
        # x = token.ent_type_

        # remove named entities
        x = ""
    if token.is_stop and (token.pos_ not in RETAINED_STOPWORD_POS):
        x = ""
    if token.pos_ not in RETAINED_POS:
        # remove stop words, except RETAINED_POS
        x = ""
    # remove single character tokens
    if len(x.strip()) == 1:
        x = ""
    x = x.strip()
    return x
