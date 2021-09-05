import json
import string
import random
import functools
import operator

from .constants import START, END, METADATA, CHILDREN

class Graph(object):
    def __init__(self, input='', textParser=None):
        self.graph = {START: {METADATA: {'count': 0}, CHILDREN: {}}}
        if input:
            self.loadJson(input)
        self.textParser = textParser if textParser else Graph.defaultTextParser
    
    def __len__(self):
        return len(self.graph)
    
    def loadJson(self, input, filename=True):
        self.graph = json.load(open(input)) if filename else json.loads(input)
    
    def saveJson(self, output, filename=True):
        if filename:
            json.dump(self.graph, open(output, 'w'))
        else:
            return json.dumps(self.graph)
    
    def getWordsByFrequency(self, top=0):
        result = [x for x in sorted(self.graph, key=lambda x: self.graph[x][METADATA]['count'], reverse=True)]
        if top:
            return result [:top]
        else:
            return result


    def learnSequence(self, seq):
        previous = START
        for each in seq:
            # update graph children
            if each in self.graph[previous][CHILDREN]:
                self.graph[previous][CHILDREN][each] += 1
            else:
                self.graph[previous][CHILDREN][each] = 1
            previous = each
            if previous not in self.graph:
                self.graph[previous] = {METADATA: {'count': 1}, CHILDREN: {}}

            #update metadata
            if each in self.graph:
                self.graph[each][METADATA]['count'] += 1
            else:
                self.graph[each][METADATA]['count'] = 1

        if END in self.graph[previous][CHILDREN]:
            self.graph[previous][CHILDREN][END] += 1
        else:
            self.graph[previous][CHILDREN][END] = 1
    
    def generateSequence(self):
        result = []
        previous = START
        while previous != END:
            current = random.choice(functools.reduce(operator.iconcat, [[x]*self.graph[previous][CHILDREN][x] for x in self.graph[previous][CHILDREN]], []))
            if current == END:
                break
    
            result.append(current)
            previous = current
        
        return ' '.join(result)

    def loadRawText(self, input, filename=True):
        if filename:
            for rawText in open(input).readlines():
                self.learnSequence(self.textParser(rawText))
        else:
            self.learnSequence(self.textParser(input))
    
    @staticmethod 
    def defaultTextParser(rawText):
        return  [x.lower() for x in rawText.translate(str.maketrans('', '', string.punctuation)).split()]
        



