"""

This file contains a function `ztz_similarity(ztz1, ztz2)`
that returns the similarity of sentences `ztz1` and `ztz2`.
ztz = sentence

It uses

Ref:
1. https://www.sbert.net/
2. https://huggingface.co/tasks/sentence-similarity
3. https://towardsdatascience.com/bert-for-measuring-text-similarity
-eec91c6bf9e1
"""
from sklearn.metrics.pairwise import cosine_similarity


def ztz_similarity(ztz1, ztz2, **kwargs):
    """
    This method returns the similarity between sentences `ztz1` and `ztz2`.
    The similarity is measured as odds of a probability, so it ranges from 0
    to infinity.

    Parameters
    ----------
    ztz1: str
    ztz2: str
    kwargs: dict[]

    Returns
    -------
    float

    """
    model = kwargs['model']
    embedding_1 = model.encode(ztz1)
    embedding_2 = model.encode(ztz2)

    prob = cosine_similarity([embedding_1], [embedding_2])[0, 0]
    if prob < 0:
        # print("neg. prob.=", prob)
        # print(ztz1)
        # print(ztz2)
        prob = 0
    odds = prob / (1 - prob) if prob < 1 else 1e5
    return round(odds, 3)
