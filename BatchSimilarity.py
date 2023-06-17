import importlib as imp
from my_globals import *
simi = imp.import_module(SIMI_DEF)
from sklearn.metrics.pairwise import cosine_similarity


class BatchSimilarity:
    """

    """
    def __init__(self, ztz1, all_ztz2, model=None):
        self.ztz1 = ztz1
        self.all_ztz2 = all_ztz2
        self.model = model
        if model:
            sent_embeddings = model.encode([ztz1] + all_ztz2)
            self.cos_vec = cosine_similarity([sent_embeddings[0]],
                              sent_embeddings[1:])[0]

    def simi(self, ztz2):
        if not self.model:
            return simi.ztz_similarity(self.ztz1, ztz2)
        else:
            i = ztz2.index(self.all_ztz2)
            prob = self.cos_vec[i]
            if prob < 0:
                # print("neg. prob.=", prob)
                # print(ztz1)
                # print(ztz2)
                prob = 0
            odds = prob / (1 - prob) if prob < 1 else 1e5
            return round(odds, 3)
