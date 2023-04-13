import spacy
import re
from unidecode import unidecode

nlp = spacy.load("en_core_web_sm")


def simplify_zntz(sentence, verbose=False):
    doc = nlp(sentence)
    clauses = []
    current_clause = []

    for token in doc:
        if token.dep_ == "mark" or token.dep_ == "cc":
            clauses.append(current_clause)
            current_clause = []
        current_clause.append(token)

    clauses.append(current_clause)

    propositions = []
    for clause in clauses:
        prop = " ".join([token.text for token in clause])
        # this replaces unicode curly quotes by ascii straight quotes
        prop = unidecode(prop)
        prop = re.sub(r'[.?!"]', '', prop)
        prop = prop.strip()
        if len(prop)>1:
            if prop[-1] ==",":
                prop = prop[:-1].strip()
            propositions.append(prop)
    if verbose:
        print(propositions)
    return propositions
