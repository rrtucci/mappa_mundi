from Dag import *
import os
from zntz_distance import ztnz_similarity
from itertools import product


def get_all_txt_titles(txt_dir):
    return [file_name[:-len(".txt")]
            for file_name in os.listdir(txt_dir)]

def get_all_dag_titles(dag_dir):
    return [file_name[:-len(".skops")]
            for file_name in os.listdir(dag_dir)]

class DagAtlas:
    def __init__(self, txt_dir, dag_dir, least_sim=.3):
        self.txt_dir = txt_dir
        self.dag_dir = dag_dir
        self.least_sim = least_sim

    def update_gains_for_two_m_titles(self, title1, title2):
        all_dag_titles = get_all_dag_titles(self.dag_dir)

        if title1 not in all_dag_titles:
            dag1 = Dag(title1, txt_dir=self.txt_dir)
        else:
            dag1 = Dag(title1, dag_dir=self.dag_dir)

        if title2 not in all_dag_titles:
            dag2 = Dag(title2, txt_dir=self.txt_dir)
        else:
            dag2 = Dag(title2, dag_dir=self.dag_dir)

        nd1_nd2_pairs = []
        for nd1, nd2 in product(dag1.nodes, dag2.nodes):
                    if ztnz_similarity(nd1.zntz, nd2.zntz) > self.least_sim:
                        nd1_nd2_pairs.append((nd1, nd2))
        nodes1, nodes2 = list(zip(*nd1_nd2_pairs))
        nodes1, nodes2 = set(nodes1), set(nodes2)

        for nd1a, nd1b in product(nodes1, nodes1):
            if nd1a.id_num < nd1b.id_num:
                nd1a_matches = set([nd2 in nodes2 for (nd1a, nd2) in \
                        nd1_nd2_pairs])
                nd2b_matches = set([nd2 in nodes2 for (nd1b, nd2) in \
                        nd1_nd2_pairs])
                for nd2a, nd2b in product(nd1a_matches, nd2b_matches):
                    if nd2a.id_num < nd2b.id_num:
                        dag1.update_gains((nd1a.id_num,
                                           nd1b.id_num))
                        dag2.update_gains((nd2a.id_num,
                                           nd2b.id_num))
        dag1.save_self(self.dag_dir)
        dag2.save_self(self.dag_dir)
            
    def update_gains_for_m_titles_list(self, titles_list=None):
        all_titles = get_all_txt_titles(self.txt_dir)
        if titles_list is None:
            titles_list = all_titles
        assert set(titles_list).issubset(set(all_titles))
        title_ids = [all_titles.index(title) for title in titles_list]
        num = len(titles_list)
        for i, j in product(range(num), range(num)):
            if i < j:
                self.update_gains_for_two_m_titles(title_ids[i],
                                                   title_ids[j])
    def update_gains_for_all_m_titles(self):
        self.update_gains_for_m_titles_list()
        