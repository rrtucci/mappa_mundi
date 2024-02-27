"""

This file contains one of several implementations of the function
`simplify_ztz(sentence, verbose=False)` that we considered.

Refs:
https://spacy.io/usage/spacy-101/

https://github.com/mmxgn/spacy-clausieec13/splitting-sentences-into-clauses
"""
from globals import *
import spacy
import claucy

nlp = spacy.load('en_core_web_sm')
claucy.add_to_pipe(nlp)


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

    doc = nlp(sentence.strip())
    if doc._.clauses:
        propositions = doc._.clauses[0].to_propositions(as_text=True)
    else:
        propositions = [sentence]
    if verbose:
        print(sentence.strip())
        print(propositions)
    return propositions
