# 1. nltk
# NLTK was unable to find stanford-parser\.jar! Set the CLASSPATH
#   environment variable.
# https://stackoverflow.com/questions/13883277/how-to-use-stanford-parser-in-nltk-using-python

from nltk.parse.stanford import StanfordParser
parser = StanfordParser()

from nltk.parse.stanford import GenericStanfordParser
parser = GenericStanfordParser()

# 2. nltk.parse.corenlp
# AttributeError: 'CoreNLPParser' object has no attribute 'tagged_parse'https://stackoverflow.com/questions/39320782/corenlp-provide-pos-tags
import nltk
from nltk.parse.corenlp import CoreNLPParser
parser = CoreNLPParser(url='http://localhost:9000')


# 3. pycorenlp
from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
parser = nlp.parse()

