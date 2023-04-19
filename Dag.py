import os

from Node import *
from skops.io import dump, load, get_untrusted_types
# https://skops.readthedocs.io/en/stable/
from my_globals import *
from DotTool import *

class Dag:
    def __init__(self, m_title, simp_ztz_dir=None, dag_dir=None):
        self.m_title = m_title

        if simp_ztz_dir and not dag_dir: # dsg file doesn't exist yet
            path = simp_ztz_dir + "/" + m_title + ".txt"
            with open(path, "r") as f:
                lines = [line for line in f]
            self.nodes = []
            for time, line in enumerate(lines):
                num_places = len(line.split(ZTZ_SEPARATOR))
                for place in range(num_places):
                    self.nodes.append(Node(time, place))
            self.arrows = []
            self.arrow_to_reps = {}
            for node in self.nodes:
                prev_nodes=[]
                for prev_nd in self.nodes:
                    if prev_nd.time > node.time:
                        if prev_nd.time == node.time -1:
                            prev_nodes.append(prev_nd)
                    else:
                        break
                for prev_nd in prev_nodes:
                    new_arrow = (prev_nd, node)
                    self.arrows.append(new_arrow)
                    self.arrow_to_reps[new_arrow] = 1
        elif not simp_ztz_dir and dag_dir: # dag file already exists
            path = dag_dir + "/" + m_title + ".skops"
            unknown_types = get_untrusted_types(file=path)
            # print("unknown types:", unknown_types)
            load(path, trusted=unknown_types)
        else:
            assert False

    def save_self(self, dag_dir):
        path = dag_dir + "/" + self.m_title + ".skops"
        dump(self, path)

    def update_arrow(self, arrow, change):
        if arrow not in self.arrows:
            self.arrows.append(arrow)
            self.arrow_to_reps[arrow] = change
        else:
            self.arrow_to_reps[arrow] += change
            # change can be negative.
            # negative changes can accumulate to
            # make arrow_to_reps[arrow] == 0
            if self.arrow_to_reps[arrow] == 0:
                self.arrows.remove(arrow)
                del self.arrow_to_reps[arrow]

    def get_node_to_prep_ztz_dict(self, remove_dialog=False):
        prep_dir = CLEAN_DIR if not remove_dialog else CLEAN_RD_DIR

        time_to_prep_ztz = {}
        with open(prep_dir, "r") as f:
            time = 0
            for line in f:
                time_to_prep_ztz[time] = line
                time += 1

        nd_to_prep_ztz = {}
        for nd in self.nodes:
            nd_to_prep_ztz[nd] = time_to_prep_ztz[nd.time]

        return nd_to_prep_ztz

    def get_node_to_simple_ztz_dict(self, remove_dialog=False):
        simp_dir = SIMP_DIR if not remove_dialog else SIMP_RD_DIR

        time_to_simp_ztz_list = {}
        with open(simp_dir, "r") as f:
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

    @staticmethod
    def arrow_str(arrow):
        return '"' + arrow[0].coords() + '"' +\
            "->" + \
            '"' + arrow[1].coords() + '"'

    def draw(self, reps_threshold, jupyter=False):
        hr_arrows = self.get_high_reps_arrows(reps_threshold)

        dot = "digraph {\n"
        for arrow in hr_arrows:
            reps = round(self.arrow_to_reps[arrow], 2)
            dot += Dag.arrow_str(arrow) + \
                   ' [label=' + str(reps) + "];\n"
        dot += "}\n"
        DotTool.draw(dot, jupyter=jupyter)















