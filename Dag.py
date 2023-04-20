import os
from Node import *
# from skops.io import dump, load, get_untrusted_types
# https://skops.readthedocs.io/en/stable/
from pickle import load, dump
from my_globals import *
from DotTool import *

class Dag:
    def __init__(self, m_title, simp_dir, preconnected=False):
        self.m_title = m_title
        path = simp_dir + "/" + m_title + ".txt"
        with open(path, "r") as f:
            lines = [line for line in f]
        self.nodes = []
        for time, line in enumerate(lines):
            if line[0] == ZTZ_SEPARATOR:
                line = line[1:]
            if line and line[-1] == ZTZ_SEPARATOR:
                line = line[:-1]
            if line:
                ztz_list = line.split(ZTZ_SEPARATOR)
                for place in range(len(ztz_list)):
                    self.nodes.append(Node(time, place))
        self.arrows = []
        self.arrow_to_reps = {}
        if preconnected:
            for node in self.nodes:
                prev_nodes=[]
                for prev_nd in self.nodes:
                    if prev_nd.time < node.time:
                        if prev_nd.time == node.time -1:
                            prev_nodes.append(prev_nd)
                    else:
                        break
                for prev_nd in prev_nodes:
                    new_arrow = (prev_nd, node)
                    self.arrows.append(new_arrow)
                    self.arrow_to_reps[new_arrow] = 1



    def save_self(self, dag_dir):
        path = dag_dir + "/" + self.m_title + ".pkl"
        with open(path, "wb") as f:
            dump(self, f)

    def update_arrow(self, arrow, change):
        if arrow not in self.arrows:
            self.arrows.append(arrow)
            self.arrow_to_reps[arrow] = change
        else:
            self.arrow_to_reps[arrow] += change
        # change can be negative.
        # negative changes can accumulate to
        # make arrow_to_reps[arrow] <= 0
        if self.arrow_to_reps[arrow] <= 0:
            self.arrows.remove(arrow)
            del self.arrow_to_reps[arrow]

    def build_node_to_clean_ztz_dict(self, clean_dir):
        path = clean_dir + "/" + self.m_title + ".txt"

        time_to_clean_ztz = {}
        with open(path, "r") as f:
            time = 0
            for line in f:
                time_to_clean_ztz[time] = line
                time += 1

        nd_to_clean_ztz = {}
        for nd in self.nodes:
            nd_to_clean_ztz[nd] = time_to_clean_ztz[nd.time]

        return nd_to_clean_ztz

    def build_node_to_simple_ztz_dict(self, simp_dir):
        path = simp_dir + "/" + self.m_title + ".txt"

        time_to_simp_ztz_list = {}
        with open(path, "r") as f:
            time = 0
            for line in f:
                time_to_simp_ztz_list[time] =\
                    line.split(ZTZ_SEPARATOR)
                time += 1

        nd_to_simp_ztz = {}
        for nd in self.nodes:
            nd_to_simp_ztz[nd] =\
                time_to_simp_ztz_list[nd.time][nd.place]
        return nd_to_simp_ztz

    def get_high_reps_arrows(self, reps_treshold):
        high_reps_arrows = []
        for arrow in self.arrows:
            if self.arrow_to_reps[arrow] >= reps_treshold:
                high_reps_arrows.append(arrow)

        return high_reps_arrows

    def draw(self, reps_threshold, jupyter=False):
        hr_arrows = self.get_high_reps_arrows(reps_threshold)

        dot = "digraph {\n"
        for arrow in hr_arrows:
            reps = round(self.arrow_to_reps[arrow], 2)
            dot += arrow_str(arrow) + \
                   ' [label=' + str(reps) + "];\n"
        dot += "}\n"
        DotTool.draw(dot, jupyter=jupyter)

if __name__ == "__main__":
    def main1(reps_threshold):
        dag_dir = "short_stories_dag_atlas"
        file_names = [file_name for
                      file_name in os.listdir(dag_dir)]
        dags = []
        for fname in file_names:
            path = dag_dir + "/" + fname
            # print("ghty", path)
            with open(path, "rb") as f:
                dag = load(f)
                dags.append(dag)
        for dag in dags:
            print(dag.m_title)
            hreps_arrows = dag.get_high_reps_arrows(
                reps_threshold)
            print({arrow_str(arrow):dag.arrow_to_reps[arrow] \
                   for arrow in hreps_arrows})
            print()

    main1(reps_threshold=10)
















