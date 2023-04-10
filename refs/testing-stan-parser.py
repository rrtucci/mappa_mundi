"""
Reference:
https://towardsdatascience.com/natural-language-processing-using-stanfords-corenlp-d9e64c1e1024

"""
import os
import subprocess
version = subprocess.check_output(
    ['java', '-version'], stderr=subprocess.STDOUT)
print("java version=\t", version)
print("CLASSPATH=\t", os.environ['CLASSPATH'])
print("STANFORD_MODELS=\t", os.environ['STANFORD_MODELS'])
print("JAVA_HOME=\t", os.environ['JAVA_HOME'])

def main1():
    from pycorenlp import StanfordCoreNLP
    nlp = StanfordCoreNLP('http://localhost:9000')

    text = "This movie was actually neither that funny, nor super witty. The movie was meh. I liked watching that movie. If I had a choice, I would not watch that movie again."
    result = nlp.annotate(text,
                       properties={
                           'annotators': 'sentiment, ner, pos',
                           'outputFormat': 'json',
                           'timeout': 1000,
                       })
    print(result)

def main2():
    #ttps://www.nltk.org/api/nltk.parse.corenlp.html
    import nltk
    from nltk.parse.corenlp import CoreNLPParser

    # Start the CoreNLP server
    # nltk.download('punkt')
    # nltk.download('corenlp')
    parser = CoreNLPParser(url='http://localhost:9000')

    # Parse a sentence
    sentence = "The quick brown fox jumps over the lazy dog."
    parse_tree = list(
        parser.parse(sentence.split())
        )[0]
    print(parse_tree)

def main3():
    import nltk
    from nltk.parse.corenlp import CoreNLPParser

    # Start the CoreNLP server
    parser = CoreNLPParser(url='http://localhost:9000', tagtype='pos')

    # Parse a tagged sentence
    tagged_sentence = [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'),
                       ('fox', 'NN'),
                       ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'),
                       ('lazy', 'JJ'),
                       ('dog', 'NN'), ('.', '.')]
    # parse_tree = list(parser.parse(tagged_sentence))[0]
    # print(parse_tree)
    parser.parse(tagged_sentence)

if __name__ == "__main__":
    # main1()
    main2()
    # main3() # doesn't work

