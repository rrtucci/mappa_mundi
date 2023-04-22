from Dag import *
import os
import sys
from itertools import product
from my_globals import *
import importlib as imp
simi = imp.import_module(SIMI_DEF)
import pickle as pik
from time import time

class DagAtlas:
    def __init__(self, simp_dir, dag_dir,
                 preconnected=False, fresh_start=True):
        self.start_time = time()
        time_now = (time() - self.start_time) / 60
        print(f"Initiating DagAtlas object: {time_now:.2f} minutes\n")

        self.simp_dir = simp_dir
        self.dag_dir = dag_dir
        self.preconnected = preconnected
        all_simp_titles = [file_name[:-len(".txt")] for\
            file_name in os.listdir(self.simp_dir)]
        self.title_to_w_permission = {}
        for title in all_simp_titles:
            self.title_to_w_permission[title] = True
        if not fresh_start:
            all_dag_titles = [file_name[:-len(".txt")] for \
                               file_name in os.listdir(self.dag_dir)]
            for title in all_dag_titles:
                assert title in all_simp_titles
                self.title_to_w_permission[title] = False


    def update_arrows_for_two_m_titles(self, title1, title2):
        time_now = (time() - self.start_time) / 60
        print(f"Starting comparison of 2 titles: {time_now:.2f} minutes")

        if self.title_to_w_permission[title1]:
            dag1 = Dag(title1, simp_dir=self.simp_dir,
                       preconnected=self.preconnected)
        else:
            path1 = self.dag_dir + "/" + title1 + ".pkl"
            try:
                with open(path1, "rb") as f:
                    dag1 = pik.load(f)
            except OSError:
                print("This file is probably missing:", path1)
                sys.exit()

        if self.title_to_w_permission[title2]:
            dag2 = Dag(title2, simp_dir=self.simp_dir,
                       preconnected=self.preconnected)
        else:
            path2 = self.dag_dir + "/" + title2 + ".pkl"
            try:
                with open(path2, "rb") as f:
                    dag2 = pik.load(f)
            except OSError:
                print("This file is probably missing:", path2)
                sys.exit()
        node_to_simple_ztz1 = \
            dag1.build_node_to_simple_ztz_dict(self.simp_dir)
        node_to_simple_ztz2 = \
            dag2.build_node_to_simple_ztz_dict(self.simp_dir)

        print("title1 and its num of nodes:", title1, len(dag1.nodes))
        print("title2 and its num of nodes:", title2, len(dag2.nodes))
        print("product of numbers of nodes=",
              len(dag1.nodes) * len(dag2.nodes))

        time_now = (time()-self.start_time)/60
        print(f"Starting bridges: {time_now:.2f} minutes")

        nd1_nd2_bridges = []
        bridge_count=0
        for nd1, nd2 in product(dag1.nodes, dag2.nodes):
            ztz1 = node_to_simple_ztz1[nd1]
            ztz2 = node_to_simple_ztz2[nd2]
            if simi.ztz_similarity(ztz1, ztz2) > SIMI_THRESHOLD:
                nd1_nd2_bridges.append((nd1, nd2))
                bridge_count += 1
                print(bridge_count, "bridges")
        ran = range(len(nd1_nd2_bridges))
        for i,j in product(ran, ran):
            if i<j:
                bridge_a = nd1_nd2_bridges[i]
                bridge_b = nd1_nd2_bridges[j]
                time_gap1 = bridge_a[0].time - bridge_b[0].time
                time_gap2 = bridge_a[1].time - bridge_b[1].time
                bridges_do_not_cross = (time_gap1*time_gap2 >0)
                if bridges_do_not_cross:
                    if time_gap1>0:
                        arrow1 = (bridge_b[0], bridge_a[0])
                        arrow2 = (bridge_b[1], bridge_a[1])
                    else:
                        arrow1 = (bridge_a[0], bridge_b[0])
                        arrow2 = (bridge_a[1], bridge_b[1])
                    assert arrow1[0].time < arrow1[1].time
                    assert arrow2[0].time < arrow2[1].time
                    dag1.update_arrow(arrow1, change=1)
                    dag2.update_arrow(arrow2, change=1)
        time_now = (time()-self.start_time)/60
        print(f"Before saving 2 dags: {time_now:.2f} minutes")
        dag1.save_self(self.dag_dir)
        self.title_to_w_permission[title1] = False
        dag2.save_self(self.dag_dir)
        self.title_to_w_permission[title2] = False

        time_now = (time()-self.start_time)/60
        print(f"Exiting 2 titles comparison: {time_now:.2f} minutes\n")
            
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
        simp_dir = "short_stories_simp"
        dag_dir = "short_stories_dag_atlas"
        atlas = DagAtlas(simp_dir, dag_dir)
        all_titles = [file_name[:-len(".txt")] \
                      for file_name in os.listdir(simp_dir)]
        atlas.update_arrows_in_batch_of_m_scripts(
            batch_titles=all_titles[0:3])
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
