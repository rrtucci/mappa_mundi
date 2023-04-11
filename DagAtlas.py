from Dag import *
import os
from zntz_distance import ztnz_similarity
from itertools import product

class DagAtlas:
    def __init__(self, txt_dir, dag_dir, simi_threshold=SIMI_THRESHOLD):
        self.txt_dir = txt_dir
        self.dag_dir = dag_dir
        self.simi_threshold = simi_threshold

    def update_arrows_for_two_m_titles(self, title1, title2):
        all_dag_titles = [file_name[:-len(".skops")]
            for file_name in os.listdir(self.dag_dir)]

        if title1 not in all_dag_titles:
            dag1 = Dag(title1, simp_zntz_dir=self.txt_dir)
        else:
            dag1 = Dag(title1, dag_dir=self.dag_dir)

        if title2 not in all_dag_titles:
            dag2 = Dag(title2, simp_zntz_dir=self.txt_dir)
        else:
            dag2 = Dag(title2, dag_dir=self.dag_dir)

        nd1_nd2_pairs = []
        for nd1, nd2 in product(dag1.nodes, dag2.nodes):
                    if ztnz_similarity(nd1.zntz, nd2.zntz)\
                            > self.simi_threshold:
                        nd1_nd2_pairs.append((nd1, nd2))
        nodes1, nodes2 = list(zip(*nd1_nd2_pairs))
        # remove repeats
        nodes1, nodes2 = list(set(nodes1)), list(set(nodes2))

        for nd1a, nd1b in product(nodes1, nodes1):
            if nd1a.time < nd1b.time:
                nd1a_matches = set([nd2 in nodes2 for (nd1a, nd2) in \
                        nd1_nd2_pairs])
                nd1b_matches = set([nd2 in nodes2 for (nd1b, nd2) in \
                        nd1_nd2_pairs])
                for nd2a, nd2b in product(nd1a_matches, nd1b_matches):
                    if nd2a.time < nd2b.time:
                        dag1.update_arrow((nd1a, nd1b))
                        dag2.update_arrow((nd2a, nd2b))
        dag1.save_self(self.dag_dir)
        dag2.save_self(self.dag_dir)
            
    def update_arrows_for_batch_of_m_scripts(self, titles_list=None):
        all_titles = [file_name[:-len(".txt")]
            for file_name in os.listdir(self.txt_dir)]

        if titles_list is None:
            titles_list = all_titles
        assert set(titles_list).issubset(set(all_titles))
        assert len(titles_list)>=2
        title_ids = [all_titles.index(title) for title in titles_list]
        num = len(titles_list)
        for i, j in product(range(num), range(num)):
            if i < j:
                self.update_arrows_for_two_m_titles(title_ids[i],
                                                    title_ids[j])
