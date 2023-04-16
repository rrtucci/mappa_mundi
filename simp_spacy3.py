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

nlp = spacy.load("en_core_web_sm")


def simplify_ztz(sentence, verbose=False):
    doc = nlp(sentence)
    clauses = []
    current_clause = []

    for token in doc:
        if token.dep_ == "mark" or token.dep_ == "cc" or token.text==";":
            clauses.append(current_clause)
            current_clause = []
        current_clause.append(token)

    clauses.append(current_clause)

    propositions = []
    for clause in clauses:
        # remove all tokens that are stopwords except
        # those with POS = "ADP', which I want to keep
        # print("ffgh", clause[0].pos_)
        prop = " ".join([token.text for token in clause\
                         if (not token.is_stop) or\
                        token.pos_=="ADP"])
        # delete .?!";
        prop = re.sub(r'[.?!";]', '', prop)
        prop = prop.strip()
        if len(prop)>1:
            # remove starting and ending commas
            if prop[-1] ==",":
                prop = prop[:-1].strip()
            if prop[0] ==",":
                prop = prop[1:].strip()
            propositions.append(prop)
    if verbose:
        print(sentence.strip())
        print(propositions)
    return propositions
