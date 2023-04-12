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

        node_to_simple_zntz1 = dag1.get_node_to_simple_zntz_dict()
        node_to_simple_zntz2 = dag2.get_node_to_simple_zntz_dict()

        nd1_nd2_pairs = []
        for nd1, nd2 in product(dag1.nodes, dag2.nodes):
            ztnz1 = node_to_simple_zntz1[nd1]
            ztnz2 = node_to_simple_zntz1[nd2]
            if ztnz_similarity(ztnz1, ztnz2) > self.simi_threshold:
                nd1_nd2_pairs.append((nd1, nd2))
        nodes1, nodes2 = list(zip(*nd1_nd2_pairs))
        # remove repeats
        nodes1 = list(set(nodes1))
        nodes2 = list(set(nodes2))

        for nd1a, nd1b in product(nodes1, nodes1):
            if nd1a.time < nd1b.time:
                nd1a_matches = set([nd2 in nodes2 for (nd1a, nd2) in \
                        nd1_nd2_pairs])
                nd1b_matches = set([nd2 in nodes2 for (nd1b, nd2) in \
                        nd1_nd2_pairs])
                for nd2a, nd2b in product(nd1a_matches, nd1b_matches):
                    if nd2a.time < nd2b.time:
                        change = 1
                    elif nd2a.time > nd2b.time:
                        change = -PENALTY
                    else:
                        change = 0
                    dag1.update_arrow((nd1a, nd1b), change)
                    dag2.update_arrow((nd2a, nd2b), change)

        dag1.save_self(self.dag_dir)
        dag2.save_self(self.dag_dir)
            
    def update_arrows_in_batch_of_m_scripts(self, batch_titles=None):
        all_titles = [file_name[:-len(".txt")]
            for file_name in os.listdir(self.txt_dir)]

        if batch_titles is None:
            batch_titles = all_titles
        assert set(batch_titles).issubset(set(all_titles))
        assert len(batch_titles) >= 2
        title_ids = [all_titles.index(title) for title in batch_titles]
        num = len(batch_titles)
        for i, j in product(range(num), range(num)):
            if i < j:
                self.update_arrows_for_two_m_titles(title_ids[i],
                                                    title_ids[j])
if __name__ == "__main__":
    def main():
        remove_dialog = True
        atlas = DagAtlas(
            txt_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
            dag_dir= DAG_DIR,
            simi_threshold=SIMI_THRESHOLD)
        all_titles = [file_name[:-len(".txt")] \
                      for file_name in os.listdir(M_SCRIPTS_DIR)]
        atlas.update_arrows_in_batch_of_m_scripts(
            batch_titles=all_titles[0:2])