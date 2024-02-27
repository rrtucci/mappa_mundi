import importlib as imp
from my_globals import *
from Dag import *

simi_def = imp.import_module(SIMI_DEF)
from sklearn.metrics.pairwise import cosine_similarity


class BatchSimilarity:
    """
    With sentence transformers, one can speed up the evaluation of sentence
    similarity by embedding large batches of sentences all at once, rather
    than one at a time. Given two DAGs, dag1 and dag2, this class uses a
    sentence transformer to evaluate the similarity between all sentences
    `all_ztz1` in dag1 and all the sentences `all_ztz2` in dag2. (ztz =
    sentence). `all_ztz1 + all_ztz2` are embedded as a batch, in a single
    shot.

    Attributes
    ----------
    all_ztz1: list[str]
    all_ztz2: list[str]
    cos_mat: np.array[float]
        a matrix of cosines corresponding to all_ztz1 X all_ztz2
    model: SentenceTransformer
    node_to_simple_ztz1: dict[Node, str]
    node_to_simple_ztz2: dict[Node, str]

    """

    def __init__(self,
                 dag1,
                 dag2,
                 node_to_simple_ztz1,
                 node_to_simple_ztz2,
                 model=None):
        """
        Constructor

        Parameters
        ----------
        dag1: Dag
        dag2: Dag
        node_to_simple_ztz1: dict[Node, str]
        node_to_simple_ztz2: dict[Node, str]
        model: SentenceTransformer
        """
        self.node_to_simple_ztz1 = node_to_simple_ztz1
        self.node_to_simple_ztz2 = node_to_simple_ztz2
        self.all_ztz1 = [node_to_simple_ztz1[nd] for nd in dag1.nodes]
        self.all_ztz2 = [node_to_simple_ztz2[nd] for nd in dag2.nodes]
        self.model = model
        if model:
            sent_embeddings = model.encode(self.all_ztz1 + self.all_ztz2)
            len1 = len(self.all_ztz1)
            self.cos_mat = cosine_similarity(sent_embeddings[:len1],
                                             sent_embeddings[len1:])

    def simi(self, nd1, nd2):
        """
        This method returns the similarity of the sentences corresponding to
        nodes `nd1` and `nd2`.

        Parameters
        ----------
        nd1: Node
        nd2: Node

        Returns
        -------
        float

        """
        ztz1 = self.node_to_simple_ztz1[nd1]
        ztz2 = self.node_to_simple_ztz2[nd2]
        if not self.model:
            return simi_def.ztz_similarity(ztz1, ztz2)
        else:
            k1 = self.all_ztz1.index(ztz1)
            k2 = self.all_ztz2.index(ztz2)
            prob = self.cos_mat[k1, k2]
            if prob < 0:
                # print("neg. prob.=", prob)
                # print(ztz1)
                # print(ztz2)
                prob = 0
            odds = prob / (1 - prob) if prob < 1 else 1e5
            return round(odds, 3)
