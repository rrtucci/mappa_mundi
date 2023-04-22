import os
from Node import *
# from skops.io import dump, load, get_untrusted_types
# https://skops.readthedocs.io/en/stable/
import pickle as pik
from my_globals import *

import graphviz as gv
from IPython.display import display, Image
from PIL.Image import open as open_image

class Dag:
    def __init__(self, m_title, simp_dir, preconnected=False):
        self.m_title = m_title
        path = simp_dir + "/" + m_title + ".txt"
        with open(path, "r") as f:
            lines = [line for line in f]
        self.nodes = []
        for time, line in enumerate(lines):
            if line.strip() not in [ZTZ_SEPARATOR, ""]:
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
            pik.dump(self, f, protocol=pik.HIGHEST_PROTOCOL)

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
            time = -1
            for line in f:
                time += 1
                time_to_clean_ztz[time] = line.strip()

        nd_to_clean_ztz = {}
        for nd in self.nodes:
            nd_to_clean_ztz[nd] = time_to_clean_ztz[nd.time]

        return nd_to_clean_ztz

    def build_node_to_simple_ztz_dict(self, simp_dir):
        path = simp_dir + "/" + self.m_title + ".txt"

        time_to_simp_ztz_list = {}
        with open(path, "r") as f:
            time = -1
            for line in f:
                time += 1
                if line.strip() != ZTZ_SEPARATOR:
                    time_to_simp_ztz_list[time] =\
                        line.split(ZTZ_SEPARATOR)

        nd_to_simp_ztz = {}
        for nd in self.nodes:
            nd_to_simp_ztz[nd] =\
                time_to_simp_ztz_list[nd.time][nd.place].strip()

        return nd_to_simp_ztz

    def build_high_reps_arrows(self, reps_treshold):
        high_reps_arrows = []
        for arrow in self.arrows:
            if self.arrow_to_reps[arrow] >= reps_treshold:
                high_reps_arrows.append(arrow)

        return high_reps_arrows

    def print_map_legend(self, clean_dir, simp_dir, reps_threshold):
        hr_arrows = self.build_high_reps_arrows(reps_threshold)
        print("MAP LEGEND")
        print("title:", self.m_title)
        print("arrow repetitions threshold:", reps_threshold)
        print("number of arrows shown:", len(hr_arrows))
        print("number of arrows dropped:", len(self.arrows)-len(hr_arrows))

        hr_nodes = []
        for arrow in hr_arrows:
            if arrow[0] not in hr_nodes:
                hr_nodes.append(arrow[0])
            if arrow[1] not in hr_nodes:
                hr_nodes.append(arrow[1])

        hr_nodes = sorted(hr_nodes, key=lambda x: x.time)
        nd_to_clean_ztz = self.build_node_to_clean_ztz_dict(clean_dir)
        nd_to_simple_ztz = self.build_node_to_simple_ztz_dict(simp_dir)

        for nd in hr_nodes:
            print(node_str(nd) + ":")
            print("(FULL)", nd_to_clean_ztz[nd])
            print("(PART)", nd_to_simple_ztz[nd])

    @staticmethod
    def draw_dot(s, j_embed):
        """
        Using display(s) will draw the graph but will not embed it permanently
        in the notebook. To embed it permanently, must generate temporary image
        file and use Image().display(s)
        Parameters
        ----------
        s: output of graphviz Source()
        j_embed: bool
            True iff want to embed image in jupyter notebook. If you are using a
            python terminal instead of a jupyter notebook, only j_embed=False
            will draw image.
        Returns
        -------
        None
        """
        x = s.render("tempo", format='png', view=False)
        if j_embed:
            display(Image(x))
        else:
            open_image("tempo.png").show()

    def draw(self, reps_threshold, jupyter=False):
        hr_arrows = self.build_high_reps_arrows(reps_threshold)

        dot = "digraph {\n"
        for arrow in hr_arrows:
            reps = round(self.arrow_to_reps[arrow], 2)
            dot += '"' + node_str(arrow[0]) + '"' + "->" +\
                    '"' + node_str(arrow[1]) + '"' +\
                   ' [label=' + str(reps) + "];\n"
        dot +=  'labelloc="b";\n'
        dot += 'label="' + self.m_title + '";\n'
        dot += "}\n"
        # print("vvbn", dot)
        Dag.draw_dot(gv.Source(dot), j_embed=jupyter)


if __name__ == "__main__":
    def main1(reps_threshold, draw):
        dag_dir = "short_stories_dag_atlas"
        simp_dir = "short_stories_simp"
        clean_dir = "short_stories_clean"
        file_names = [file_name for
                      file_name in os.listdir(dag_dir)
                      [0:3]]
        dags = []
        for fname in file_names:
            path = dag_dir + "/" + fname
            # print("ghty", path)
            with open(path, "rb") as f:
                dag = pik.load(f)
                dags.append(dag)
        for dag in dags:
            print("-------------------------")
            print(dag.m_title)
            hreps_arrows = dag.build_high_reps_arrows(
                reps_threshold)
            print({arrow_str(arrow):dag.arrow_to_reps[arrow] \
                   for arrow in hreps_arrows})
            print()
            if draw:
                dag.draw(reps_threshold)
                dag.print_map_legend(clean_dir, simp_dir, reps_threshold)

    main1(reps_threshold=4, draw=True)
















