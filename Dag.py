from Node import *
from skops.io import dump, load, get_untrusted_types
# https://skops.readthedocs.io/en/stable/

class Dag:
    def __init__(self, m_title, txt_dir=None, dag_dir=None):
        self.m_title = m_title

        if txt_dir and not dag_dir:
            path = txt_dir + "/" + m_title + ".txt"
            with open(path, "r", encoding="utf-8") as f:
                lines = [line for line in f]
            num_nodes = len(lines)
            self.nodes = [Node(m_title, i, lines[i])
                          for i in range(num_nodes)]
            self.arrows = [(i, i+1) for i in range(num_nodes-1)]
            self.gains = [1]*(num_nodes-1)
        elif not txt_dir and dag_dir:
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
            self.gains.append(1)
        else:
            i = self.arrows.index(arrow)
            self.gains[i] += 1










