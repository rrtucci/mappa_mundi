class Node:
    def __init__(self, time, place):
        self.time = time
        self.place = place
        assert time >=0 and place >= 0

def node_str(node):
    return "(" + str(node.time) + "," + str(node.place) + ")"

def arrow_str(arrow):
    return node_str(arrow[0]) + "->" + node_str(arrow[1])





