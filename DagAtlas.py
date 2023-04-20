from Dag import *
import os
import sys
from itertools import product
from my_globals import *
import importlib as imp
simi = imp.import_module(SIMI_DEF)
from pickle import load, dump

class DagAtlas:
    def __init__(self, simp_dir, dag_dir,
                 preconnected=False):
        self.simp_dir = simp_dir
        self.dag_dir = dag_dir
        self.preconnected = preconnected
        all_simp_titles = [file_name[:-len(".txt")] for\
            file_name in os.listdir(self.simp_dir)]
        self.title_to_fresh = {}
        for title in all_simp_titles:
            self.title_to_fresh[title] = True

    def update_arrows_for_two_m_titles(self, title1, title2):
        if self.title_to_fresh[title1]:
            dag1 = Dag(title1, simp_dir=self.simp_dir,
                       preconnected=self.preconnected)
            self.title_to_fresh[title1] = False
        else:
            path1 = self.dag_dir + "/" + title1 + ".pkl"
            try:
                with open(path1, "rb") as f:
                    dag1 = load(f)
            except OSError:
                print("This file is probably missing:", path1)
                sys.exit()

        if self.title_to_fresh[title2]:
            dag2 = Dag(title2, simp_dir=self.simp_dir,
                       preconnected=self.preconnected)
            self.title_to_fresh[title2] = False
        else:
            path2 = self.dag_dir + "/" + title2 + ".pkl"
            try:
                with open(path2, "rb") as f:
                    dag2 = load(f)
            except OSError:
                print("This file is probably missing:", path2)
                sys.exit()
        node_to_simple_ztz1 = \
            dag1.build_node_to_simple_ztz_dict(self.simp_dir)
        node_to_simple_ztz2 = \
            dag2.build_node_to_simple_ztz_dict(self.simp_dir)

        nd1_nd2_bridges = []
        for nd1, nd2 in product(dag1.nodes, dag2.nodes):
            ztz1 = node_to_simple_ztz1[nd1]
            ztz2 = node_to_simple_ztz2[nd2]
            if simi.ztz_similarity(ztz1, ztz2) > SIMI_THRESHOLD:
                nd1_nd2_bridges.append((nd1, nd2))
        print("qwede*****************", len(nd1_nd2_bridges))
        if nd1_nd2_bridges:
            nodes1, nodes2 = list(zip(*nd1_nd2_bridges))
        else:
            nodes1, nodes2 = [], []
        # remove repeats
        nodes1 = list(set(nodes1))
        nodes2 = list(set(nodes2))

        for nd1a, nd1b in product(nodes1, nodes1):
            if nd1a.time < nd1b.time:
                nd1a_dag2_matches = set([nd2 for (nd1a, nd2) in nd1_nd2_bridges])
                nd1b_dag2_matches = set([nd2 for (nd1b, nd2) in nd1_nd2_bridges])
                for nd2a, nd2b in product(nd1a_dag2_matches, nd1b_dag2_matches):
                    if nd2a.time < nd2b.time:
                        change = 1
                    elif nd2a.time > nd2b.time:
                        change = -CAUSAL_MISMATCH_PENALTY
                    else:
                        change = 0
                    dag1.update_arrow((nd1a, nd1b), change)
                    dag2.update_arrow((nd2a, nd2b), change)

        dag1.save_self(self.dag_dir)
        dag2.save_self(self.dag_dir)
            
    def update_arrows_in_batch_of_m_scripts(self, batch_titles=None):
        all_simp_titles = [file_name[:-len(".txt")] for\
                      file_name in os.listdir(self.simp_dir)]

        if batch_titles is None:
            batch_titles = all_simp_titles
        assert set(batch_titles).issubset(set(all_simp_titles))
        assert len(batch_titles) >= 2
        num = len(batch_titles)

        for i, j in product(range(num), range(num)):
            if i < j:
                self.update_arrows_for_two_m_titles(batch_titles[i],
                                                    batch_titles[j])
if __name__ == "__main__":
    def main1():
        remove_dialog = False
        simp_dir = "short_stories_simp"
        dag_dir = "short_stories_dag_atlas"
        atlas = DagAtlas(simp_dir, dag_dir, preconnected=False)
        all_titles = [file_name[:-len(".txt")] \
                      for file_name in os.listdir(simp_dir)]
        # print("asdre", all_titles)
        atlas.update_arrows_in_batch_of_m_scripts(
            batch_titles=all_titles)
    def main2():
        remove_dialog = True
        atlas = DagAtlas(
            simp_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
            dag_dir= DAG_DIR)
        all_titles = [file_name[:-len(".txt")] \
                      for file_name in os.listdir(M_SCRIPTS_DIR)]
        atlas.update_arrows_in_batch_of_m_scripts(
            batch_titles=all_titles[0:2])
    main1()
