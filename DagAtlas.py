from Dag import *
from BatchSimilarity import *
from utils import *
import sys
from itertools import product
from globals import *

import pickle as pik
from time import time
from sentence_transformers import SentenceTransformer


class DagAtlas:
    """
    This class reads movie script txt files from the `out_dir` directory (
    simplified movie scripts) and creates a pickled file for each movie
    script. Each pickled file contains a Dag object for one movie. `dag_dir`
    (called the DAG atlas) is the directory containing the pickled files.
    This class is also called `DagAtlas`.

    Attributes
    ----------
    dag_dir: str
        directory where this class writes pickled files. One pickled file (
        i.e., DAG) per movie.
    model: SentenceTransformer
        Model returned by SentenceTransformer constructor
    simp_dir: str
        directory where this class reads txt files.
    start_time: float
        time in minutes when self is created.
    title_to_permission_to_write_new_pickle: dict[str, bool]
        A dictionary that maps each movie title to a boolean that grants 
        permission to overwrite an existing pickled file.

    """

    def __init__(self, simp_dir, dag_dir,
                 recycled_pickles=None):
        """
        Constructor

        Parameters
        ----------
        simp_dir: str
            directory with a simplified txt file for each movie script
        dag_dir: str
            directory with a pickled file containing a Dag object for each
            movie script
        recycled_pickles: list[str]
            titles for which overwriting of pickled files is forbidden, at the
            beginning, when self is first constructed.

        """
        self.start_time = time()
        time_now = (time() - self.start_time) / 60
        print(f"Initiating DagAtlas object: {time_now:.2f} minutes\n")

        self.simp_dir = simp_dir
        self.dag_dir = dag_dir
        all_simp_titles = [file_name[:-len(".txt")] for \
                           file_name in my_listdir(self.simp_dir)]
        all_dag_titles = [file_name[:-len(".pkl")] for \
                          file_name in my_listdir(self.dag_dir)]
        assert set(all_dag_titles).issubset(set(all_simp_titles))

        self.title_to_permission_to_write_new_pickle = {}
        for title in all_simp_titles:
            self.title_to_permission_to_write_new_pickle[title] = True
        if recycled_pickles is None:
            recycled_pickles = []
        for title in recycled_pickles:
            assert title in all_dag_titles
            self.title_to_permission_to_write_new_pickle[title] = False

        if SIMI_DEF == "similarity_bert":
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.model = None

    def update_arrows_for_two_m_scripts(self, title1, title2):
        """
        This method updates the arrows for 2 movie titles.

        Parameters
        ----------
        title1: str
        title2: str

        Returns
        -------
        None

        """
        time_now = (time() - self.start_time) / 60
        print(f"Starting comparison of 2 titles: {time_now:.2f} minutes")

        if self.title_to_permission_to_write_new_pickle[title1]:
            dag1 = Dag(title1, simp_dir=self.simp_dir)
        else:
            path1 = self.dag_dir + "/" + title1 + ".pkl"
            try:
                with open(path1, "rb") as f:
                    dag1 = pik.load(f)
            except OSError:
                print("This file is probably missing:", path1)
                sys.exit()

        if self.title_to_permission_to_write_new_pickle[title2]:
            dag2 = Dag(title2, simp_dir=self.simp_dir)
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

        time_now = (time() - self.start_time) / 60
        print(f"Starting bridges: {time_now:.2f} minutes")

        nd1_nd2_bridges = []
        bridge_count = 0
        batch_simi = BatchSimilarity(dag1, dag2,
                                    node_to_simple_ztz1,
                                    node_to_simple_ztz2,
                                    model=self.model)
        for nd1, nd2 in product(dag1.nodes, dag2.nodes):
            if batch_simi.simi(nd1, nd2) > SIMI_THRESHOLD:
                nd1_nd2_bridges.append((nd1, nd2))
                bridge_count += 1
                print(bridge_count, "bridges")
        range0 = range(len(nd1_nd2_bridges))
        for i, j in product(range0, range0):
            if i < j:
                bridge_a = nd1_nd2_bridges[i]
                bridge_b = nd1_nd2_bridges[j]
                arrows = [None, None]
                time_gaps = [0, 0]
                for movie in range(2):
                    time_gaps[movie] = \
                        bridge_a[movie].time - bridge_b[movie].time
                    if time_gaps[movie] > 0:
                        arrows[movie] = (bridge_b[movie], bridge_a[movie])
                    else:
                        arrows[movie] = (bridge_a[movie], bridge_b[movie])
                bridges_do_not_cross = (time_gaps[0] * time_gaps[1] > 0)
                if bridges_do_not_cross:
                    accepted = True
                else:
                    accepted = False
                dag1.update_arrow(arrows[0], accepted)
                dag2.update_arrow(arrows[1], accepted)

        time_now = (time() - self.start_time) / 60
        print(f"Before saving 2 dags: {time_now:.2f} minutes")
        dag1.save_self(self.dag_dir)
        self.title_to_permission_to_write_new_pickle[title1] = False
        dag2.save_self(self.dag_dir)
        self.title_to_permission_to_write_new_pickle[title2] = False

        time_now = (time() - self.start_time) / 60
        print(f"Exiting 2 titles comparison: {time_now:.2f} minutes\n")

    def update_arrows_in_batch_of_m_scripts(self, batch_titles=None):
        """
        This method calls the method `update_arrows_for_two_m_scripts` for
        every pair '{ title1, title2}' of movie scripts in the list
        `batch_titles`.

        Parameters
        ----------
        batch_titles: list[str] or None

        Returns
        -------
        None

        """
        all_simp_titles = [file_name[:-len(".txt")] for \
                           file_name in my_listdir(self.simp_dir)]

        if batch_titles is None:
            batch_titles = all_simp_titles
        assert set(batch_titles).issubset(set(all_simp_titles))
        assert len(batch_titles) >= 2
        num = len(batch_titles)

        for i, j in product(range(num), range(num)):
            if i < j:
                self.update_arrows_for_two_m_scripts(batch_titles[i],
                                                     batch_titles[j])

    def update_arrows_for_one_m_script_and_others(self,
                                                  title,
                                                  other_titles):
        """
        This method calls the method `update_arrows_for_two_m_scripts` for
        every pair '{ title, other_title}' of movie scripts,
        where `other_title` is in the list `other_titles`.

        Parameters
        ----------
        title: str
        other_titles: list[str]

        Returns
        -------
        None

        """
        all_simp_titles = [file_name[:-len(".txt")] for \
                           file_name in my_listdir(self.simp_dir)]
        assert set(other_titles).issubset(set(all_simp_titles))
        assert title not in other_titles

        for j in range(len(other_titles)):
            self.update_arrows_for_two_m_scripts(title,
                                                 other_titles[j])


if __name__ == "__main__":
    def main1():
        simp_dir = "short_stories_post_clean"
        dag_dir = "short_stories_dag_atlas"
        atlas = DagAtlas(simp_dir, dag_dir)
        all_titles = [file_name[:-len(".txt")] \
                      for file_name in my_listdir(simp_dir)]
        atlas.update_arrows_in_batch_of_m_scripts(
            batch_titles=all_titles[0:3])


    def main2():
        remove_dialog = False
        atlas = DagAtlas(
            simp_dir=POST_CLEAN_DIR if not remove_dialog else
                POST_CLEAN_RD_DIR,
            dag_dir=DAG_DIR)
        all_titles = [file_name[:-len(".txt")] \
                      for file_name in my_listdir(SIMP_DIR)]
        atlas.update_arrows_in_batch_of_m_scripts(
            batch_titles=all_titles[0:3])


    main1()
    # main2()
