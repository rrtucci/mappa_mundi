import importlib as imp
from my_globals import *

simi = imp.import_module(SIMI_DEF)
from sklearn.metrics.pairwise import cosine_similarity


class BatchSimilarity:
    """
    With sentence transformers, one can speed up the evaluation of sentence
    similarity by embedding large batches of sentences all at once, rather
    than one at a time. Given two DAGs, dag1 and dag2, this class uses a
    sentence transformer to evaluate the similarity between a single
    anchoring sentence `ztz1` in dag1 and all the sentences `all_ztz2` in
    dag2. (ztz = sentence). `[ztz1] + all_ztz2` are embedded as a batch,
    in a single shot.

    Attributes
    ----------
    all_ztz2: list[str]
    cos_vec: np.array[float]
        a vector of cosines in the same order as `all_ztz2`
    model: SentenceTransformer
    ztz1: str

    """

    def __init__(self, ztz1, all_ztz2, model=None):
        """
        Constructor

        Parameters
        ----------
        ztz1: str
        all_ztz2: list[str]
        model: SentenceTransformer
        """
        self.ztz1 = ztz1
        self.all_ztz2 = all_ztz2
        self.model = model
        if model:
            sent_embeddings = model.encode([ztz1] + all_ztz2)
            self.cos_vec = cosine_similarity([sent_embeddings[0]],
                                             sent_embeddings[1:])[0]

    def simi(self, ztz2):
        """
        This method returns the similarity of sentences `ztz1` and `ztz2`.
        ztz = sentence

        Parameters
        ----------
        ztz2: str

        Returns
        -------
        float

        """
        if not self.model:
            return simi.ztz_similarity(self.ztz1, ztz2)
        else:
            i = self.all_ztz2.index(ztz2)
            prob = self.cos_vec[i]
            if prob < 0:
                # print("neg. prob.=", prob)
                # print(ztz1)
                # print(ztz2)
                prob = 0
            odds = prob / (1 - prob) if prob < 1 else 1e5
            return round(odds, 3)
