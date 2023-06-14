'''
Created on Mar 19, 2015

@author: TPetrou
'''

from nltk.parse import stanford
import os, sys
import operator

java_path = r"C:\Program Files\Java\jdk1.8.0_31\bin\java.exe"
os.environ['JAVAHOME'] = java_path
os.environ[
    'STANFORD_PARSER'] = r'/users/ted/stanford nlp/stanford-parser-full-2015-01-30'
os.environ[
    'STANFORD_MODELS'] = r'/users/ted/stanford nlp/stanford-parser-full-2015-01-30'


class RDF_Triple():
    class RDF_SOP():

        def __init__(self, name, pos=''):
            self.name = name
            self.word = ''
            self.parent = ''
            self.grandparent = ''
            self.depth = ''
            self.predicate_list = []
            self.predicate_sibings = []
            self.pos = pos
            self.attr = []
            self.attr_trees = []

    def __init__(self, sentence):
        self.sentence = sentence
        self.clear_data()

    def clear_data(self):
        self.parser = stanford.StanfordParser(
            model_path=r"/users/ted/stanford nlp/stanford-parser-full-2015-01-30/stanford-parser-3.5.1-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        self.first_NP = ''
        self.first_VP = ''
        self.parse_tree = None
        self.subject = RDF_Triple.RDF_SOP('subject')
        self.predicate = RDF_Triple.RDF_SOP('predicate', 'VB')
        self.Object = RDF_Triple.RDF_SOP('object')

    def find_NP(self, t):
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label() == 'NP':
                if self.first_NP == '':
                    self.first_NP = t
            elif t.label() == 'VP':
                if self.first_VP == '':
                    self.first_VP = t
            for child in t:
                self.find_NP(child)

    def find_subject(self, t, parent=None, grandparent=None):
        if self.subject.word != '':
            return
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label()[:2] == 'NN':
                if self.subject.word == '':
                    self.subject.word = t.leaves()[0]
                    self.subject.pos = t.label()
                    self.subject.parent = parent
                    self.subject.grandparent = grandparent
            else:
                for child in t:
                    self.find_subject(child, parent=t, grandparent=parent)

    def find_predicate(self, t, parent=None, grandparent=None, depth=0):
        try:
            t.label()
        except AttributeError:
            pass
        else:
            if t.label()[:2] == 'VB':
                self.predicate.predicate_list.append(
                    (t.leaves()[0], depth, parent, grandparent))

            for child in t:
                self.find_predicate(child, parent=t, grandparent=parent,
                                    depth=depth + 1)

    def find_deepest_predicate(self):
        if not self.predicate.predicate_list:
            return '', '', '', ''
        return max(self.predicate.predicate_list, key=operator.itemgetter(1))

    def extract_word_and_pos(self, t, depth=0, words=[]):
        try:
            t.label()
        except AttributeError:
            #             print t
            #             print 'error', t
            pass
        else:
            # Now we know that t.node is defined
            if t.height() == 2:
                #                 self.word_pos_holder.append((t.label(), t.leaves()[0]))
                words.append((t.leaves()[0], t.label()))
            for child in t:
                self.extract_word_and_pos(child, depth + 1, words)
        return words

    def print_tree(self, t, depth=0):
        try:
            t.label()
        except AttributeError:
            print(t)
            #             print 'error', t
            pass
        else:
            # Now we know that t.node is defined
            print('(') # , t.label(), t.leaves()[0]
            for child in t:
                self.print_tree(child, depth + 1)
            print(') ')

    def find_object(self):
        for t in self.predicate.parent:
            if self.Object.word == '':
                self.find_object_NP_PP(t, t.label(), self.predicate.parent,
                                       self.predicate.grandparent)

    def find_object_NP_PP(self, t, phrase_type, parent=None, grandparent=None):
        '''
        finds the object given its a NP or PP or ADJP
        '''
        if self.Object.word != '':
            return
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label()[:2] == 'NN' and phrase_type in ['NP', 'PP']:
                if self.Object.word == '':
                    self.Object.word = t.leaves()[0]
                    self.Object.pos = t.label()
                    self.Object.parent = parent
                    self.Object.grandparent = grandparent
            elif t.label()[:2] == 'JJ' and phrase_type == 'ADJP':
                if self.Object.word == '':
                    self.Object.word = t.leaves()[0]
                    self.Object.pos = t.label()
                    self.Object.parent = parent
                    self.Object.grandparent = grandparent
            else:
                for child in t:
                    self.find_object_NP_PP(child, phrase_type, parent=t,
                                           grandparent=parent)

    def get_attributes(self, pos, sibling_tree, grandparent):
        rdf_type_attr = []
        if pos[:2] == 'JJ':
            for item in sibling_tree:
                if item.label()[:2] == 'RB':
                    rdf_type_attr.append((item.leaves()[0], item.label()))
        else:
            if pos[:2] == 'NN':
                for item in sibling_tree:
                    if item.label()[:2] in ['DT', 'PR', 'PO', 'JJ', 'CD']:
                        rdf_type_attr.append((item.leaves()[0], item.label()))
                    if item.label() in ['QP', 'NP']:
                        # append a tree
                        rdf_type_attr.append(item, item.label())
            elif pos[:2] == 'VB':
                for item in sibling_tree:
                    if item.label()[:2] == 'AD':
                        rdf_type_attr.append((item, item.label()))

        if grandparent:
            if pos[:2] in ['NN', 'JJ']:
                for uncle in grandparent:
                    if uncle.label() == 'PP':
                        rdf_type_attr.append((uncle, uncle.label()))
            elif pos[:2] == 'VB':
                for uncle in grandparent:
                    if uncle.label()[:2] == 'VB':
                        rdf_type_attr.append((uncle, uncle.label()))

        return self.attr_to_words(rdf_type_attr)

    def attr_to_words(self, attr):
        new_attr_words = []
        new_attr_trees = []
        for tup in attr:
            # if type(tup[0]) != unicode:
            #     if tup[0].height() == 2:
            #         new_attr_words.append((tup[0].leaves()[0], tup[0].label()))
            #     else:
            #         #                     new_attr_words.extend(self.extract_word_and_pos(tup[0]))
            #         new_attr_trees.append(tup[0].unicode_repr())
            # else:
                new_attr_words.append(tup)
        return new_attr_words, new_attr_trees

    def jsonify_rdf(self):
        return {'sentence': self.sentence,
                'parse_tree': self.parse_tree.unicode_repr(),
                'predicate': {'word': self.predicate.word,
                              'POS': self.predicate.pos,
                              'Word Attributes': self.predicate.attr,
                              'Tree Attributes': self.predicate.attr_trees},
                'subject': {'word': self.subject.word, 'POS': self.subject.pos,
                            'Word Attributes': self.subject.attr,
                            'Tree Attributes': self.subject.attr_trees},
                'object': {'word': self.Object.word, 'POS': self.Object.pos,
                           'Word Attributes': self.Object.attr,
                           'Tree Attributes': self.Object.attr_trees},
                'rdf': [self.subject.word, self.predicate.word,
                        self.Object.word]
                }

    def main(self):
        self.clear_data()
        self.parse_tree = self.parser.raw_parse(self.sentence)[0]
        self.find_NP(self.parse_tree)
        self.find_subject(self.first_NP)
        self.find_predicate(self.first_VP)
        if self.subject.word == '' and self.first_NP != '':
            self.subject.word = self.first_NP.leaves()[0]
        self.predicate.word, self.predicate.depth, self.predicate.parent, self.predicate.grandparent = self.find_deepest_predicate()
        self.find_object()
        self.subject.attr, self.subject.attr_trees = self.get_attributes(
            self.subject.pos, self.subject.parent, self.subject.grandparent)
        self.predicate.attr, self.predicate.attr_trees = self.get_attributes(
            self.predicate.pos, self.predicate.parent,
            self.predicate.grandparent)
        self.Object.attr, self.Object.attr_trees = self.get_attributes(
            self.Object.pos, self.Object.parent, self.Object.grandparent)
        self.answer = self.jsonify_rdf()


if __name__ == '__main__':
    # try:
    #     sentence = sys.argv[1]
    #     sentence = 'A rare black squirrel has become a regular visitor to a suburban garden'
    # except IndexError:
    #     print("Enter in your sentence")
    #     sentence = 'A rare black squirrel has become a regular visitor to a suburban garden'
    #     print("Heres an example")
    #     print(sentence)

    # sentence = 'The boy dunked the basketball'
    sentence = 'They also made the substance able to last longer in the bloodstream, which led to more stable blood sugar levels and less frequent injections.'
    #sentence = 'A rare black squirrel has become a regular visitor to a
    # suburban garden'
    rdf = RDF_Triple(sentence)
    rdf.main()

    ans = rdf.answer
    print(ans)