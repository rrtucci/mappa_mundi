"""

This file contains one of several implementations of the function
`simplify_ztz(sentence, verbose=False)` that we considered.

References

1. https://stanfordnlp.github.io/CoreNLP/openie.html#api
# Default value of openie.affinity_probability_cap was 1/3.
2. https://pypi.org/project/stanford-openie/

2. https://stanfordnlp.github.io/CoreNLP/demo.html

"""
from openie import StanfordOpenIE

properties = {
    'openie.triple.all_nominals': True,
    'openie.triple.strict': False,
    'openie.splitter.nomodel': True,
    'openie.affinity_probability_cap': 1/ 3
}
client = StanfordOpenIE(properties=properties)


def simplify_ztz(sentence, verbose=False):
    """
    This method simplifies the sentence `sentence`.

    Parameters
    ----------
    sentence: str
    verbose: bool

    Returns
    -------
    str

    """
    ztz_list = []
    for triple in client.annotate(sentence):
        ztz_list.append(triple['subject'] + " " +
                        triple['relation'] + " " +
                        triple['object'])
    if verbose:
        print(sentence.strip())
        print(ztz_list)
    return ztz_list


