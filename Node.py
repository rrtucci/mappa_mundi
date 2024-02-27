class Node:
    """

    This is a very simple class that holds the `time` and `place` of each
    node.

    Each simplified clause becomes a node of the DAG.

    For brevity, let us refer to time as `t` and place as `x`. Previously,
    we put each full sentence of the movie script into one row of a file.
    Then each sentence was replaced by zero, one, two, or more simplified
    clauses, separated by separator-tokens. If a simplified clause ( i.e.,
    node) appears at the row $t$ of the file (counting starting with 0),
    then we say that the node occurs at time $t$. If a simplified clause
    appears after zero separator-tokens, we say $x=0$ for it. If it appears
    after one separator-token, we say $x=1$ for it, and so forth. Hence each
    node ( i.e., simplified clause) can be labeled by its $(t, x)$ coordinates.

    Attributes
    ----------
    place: int
    time: int
    """

    def __init__(self, time, place):
        """
        Constructor

        Parameters
        ----------
        time: int
        place: int
        """
        self.time = time
        self.place = place
        assert time >= 0 and place >= 0

    def coords(self):
        """
        This method returns the coordinates of self as a tuple.

        Returns
        -------
        tuple(int, int)

        """
        return (self.time, self.place)


def node_str(node):
    """
    This method returns a string for Node `node`.

    Parameters
    ----------
    node: Node

    Returns
    -------
    str

    """
    return "(" + str(node.time) + "," + str(node.place) + ")"


def arrow_str(arrow):
    """
    This method returns a string for an arrow `arrow`

    Parameters
    ----------
    arrow: tuple[Node, Node]

    Returns
    -------
    str

    """
    return node_str(arrow[0]) + "->" + node_str(arrow[1])
