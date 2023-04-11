import os

from Node import *
from skops.io import dump, load, get_untrusted_types
# https://skops.readthedocs.io/en/stable/
from my_globals import *
from DotTool import *

class Dag:
    def __init__(self, m_title, simp_zntz_dir=None, dag_dir=None):
        self.m_title = m_title

        if simp_zntz_dir and not dag_dir:
            path = simp_zntz_dir + "/" + m_title + ".txt"
            with open(path, "r", encoding="utf-8") as f:
                lines = [line for line in f]
            num_nodes = len(lines)
            self.nodes = []
            for time, line in enumerate(lines):
                num_places = len(line.split(ZNTZ_SEPARATOR))
                for place in range(num_places):
                    self.nodes.append(Node(time, place))
            self.arrows = []
            for node in self.nodes:
                prev_nodes=[]
                for prev_nd in self.nodes:
                    if prev_nd.time == node.time-1:
                        prev_nodes.append(prev_nd)
                    else:
                        break
                for prev_nd in prev_nodes:
                    self.arrows.append((prev_nd, node))
            self.arrow_to_reps = {arrow: 1 for arrow in self.nodes}
        elif not simp_zntz_dir and dag_dir:
            path = dag_dir + "/" + m_title + ".skops"
            unknown_types = get_untrusted_types(file=path)
            print("unknown types:", unknown_types)
            load(path, trusted=unknown_types)
        else:
            assert False

    def save_self(self, dag_dir):
        path = dag_dir + "/" + self.m_title + ".skops"
        dump(self, path)

    def update_arrow(self, arrow):
        if arrow not in self.arrows:
            self.arrows.append(arrow)
            self.arrow_to_reps[arrow] = 1
        else:
            self.arrow_to_reps[arrow] += 1

    def get_node_to_sentences_dict(self, remove_dialog=False):
        if remove_dialog:
            prep_dir = PREP_DIR
            simp_dir = SIMP_DIR
        else:
            prep_dir = PREP_RD_DIR
            simp_dir = SIMP_RD_DIR
        prep_path = prep_dir + "/" + self.m_title + ".txt"
        simp_path = simp_dir + "/" + self.m_title + ".txt"

        time_to_prep_zntz = {}
        with open(prep_dir, "r") as f:
            time = 0
            for line in f:
                time_to_prep_zntz[time] = line
                time += 1

        nd_to_prep_zntz = {}
        for nd in self.nodes:
            nd_to_prep_zntz[nd] = time_to_prep_zntz[nd.time]

        time_to_simp_zntz_list = {}
        with open(simp_dir, "r"):
            time = 0
            for line in f:
                time_to_simp_zntz_list[time] =\
                    line.split(ZNTZ_SEPARATOR)
                time += 1

        nd_to_simp_zntz = {}
        for nd in self.nodes:
            nd_to_simp_zntz[nd] =\
                time_to_simp_zntz_list[nd.time][nd.place]
        return nd_to_prep_zntz, nd_to_simp_zntz

    def get_high_reps_arrows(self, reps_treshold):
        high_reps_arrows = []
        for arrow in self.arrows:
            if self.arrow_to_reps[arrow] >= reps_treshold:
                high_reps_arrows.append(arrow)

        return high_reps_arrows

    @staticmethod
    def arrow_str(arrow):
        return str(arrow[0].coords(), arrow[1].coords())

    def draw(self, reps_threshold, jupyter=False):
        hr_arrows = self.get_high_reps_arrows(reps_threshold)

        dot = "digraph {\n"
        for arrow in hr_arrows:
            reps = self.arrow_to_reps[arrow]
            dot += Dag.arrow_str(arrow) + \
                   ' [label=' + str(reps) + "];\n"
        dot += "}\n"
        DotTool.draw(dot, jupyter=jupyter)















