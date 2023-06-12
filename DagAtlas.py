from Dag import *
from utils import *
import sys
from itertools import product
from my_globals import *
import importlib as imp
import pickle as pik
from time import time
from sentence_transformers import SentenceTransformer

simi = imp.import_module(SIMI_DEF)


class DagAtlas:
    """
    This class reads movie script txt files from the `simp_dir` directory (
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
    preconnected: bool
        True iff all Dag objects created by this class are preconnected
    simp_dir: str
        directory where this class reads txt files.
    start_time: float
        time in minutes when self is created.
    title_to_permission_to_write_new_pickle: dict[str, bool]
        A dictionary that maps each movie title to a boolean that grants 
        permission to overwrite an existing pickled file.

    """

    def __init__(self, simp_dir, dag_dir,
                 preconnected=False, recycled_pickles=None):
        """
        Constructor

        Parameters
        ----------
        simp_dir: str
            directory with a simplified txt file for each movie script
        dag_dir: str
            directory with a pickled file containing a Dag object for each
            movie script
        preconnected: bool
            True iff all Dag objects created by this class are preconnected
        recycled_pickles: list[str]
            titles for which overwriting of pickled files is forbidden, at the
            beginning, when self is first constructed.

        """
        self.start_time = time()
        time_now = (time() - self.start_time) / 60
        print(f"Initiating DagAtlas object: {time_now:.2f} minutes\n")

        self.simp_dir = simp_dir
        self.dag_dir = dag_dir
        self.preconnected = preconnected
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

        if self.title_to_permission_to_write_new_pickle[title2]:
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

        time_now = (time() - self.start_time) / 60
        print(f"Starting bridges: {time_now:.2f} minutes")

        nd1_nd2_bridges = []
        bridge_count = 0
        for nd1, nd2 in product(dag1.nodes, dag2.nodes):
            ztz1 = node_to_simple_ztz1[nd1]
            ztz2 = node_to_simple_ztz2[nd2]
            if simi.ztz_similarity(ztz1, ztz2) > SIMI_THRESHOLD:
                nd1_nd2_bridges.append((nd1, nd2))
                bridge_count += 1
                print(bridge_count, "bridges")
        ran = range(len(nd1_nd2_bridges))
        for i, j in product(ran, ran):
            if i < j:
                bridge_a = nd1_nd2_bridges[i]
                bridge_b = nd1_nd2_bridges[j]
                time_gap1 = bridge_a[0].time - bridge_b[0].time
                time_gap2 = bridge_a[1].time - bridge_b[1].time
                bridges_do_not_cross = (time_gap1 * time_gap2 > 0)
                if bridges_do_not_cross:
                    if time_gap1 > 0:
                        arrow1 = (bridge_b[0], bridge_a[0])
                        arrow2 = (bridge_b[1], bridge_a[1])
                    else:
                        arrow1 = (bridge_a[0], bridge_b[0])
                        arrow2 = (bridge_a[1], bridge_b[1])
                    assert arrow1[0].time < arrow1[1].time
                    assert arrow2[0].time < arrow2[1].time
                    dag1.update_arrow(arrow1, change=1)
                    dag2.update_arrow(arrow2, change=1)
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
        simp_dir = "short_stories_simp"
        dag_dir = "short_stories_dag_atlas"
        atlas = DagAtlas(simp_dir, dag_dir)
        all_titles = [file_name[:-len(".txt")] \
                      for file_name in my_listdir(simp_dir)]
        atlas.update_arrows_in_batch_of_m_scripts(
            batch_titles=all_titles[0:3])


    def main2():
        remove_dialog = False
        atlas = DagAtlas(
            simp_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
            dag_dir=DAG_DIR)
        all_titles = [file_name[:-len(".txt")] \
                      for file_name in my_listdir(SIMP_DIR)]
        atlas.update_arrows_in_batch_of_m_scripts(
            batch_titles=all_titles[0:3])


    # main1()
    main2()
