__author__ = 'mengpeng'
import nltk
from trie import Trie
from util.mongo_juice import MongoJuice
from collections import Counter


class Recipe(object):

    def __init__(self):
        self.id = ''
        self.url = ''
        self.name = ''
        self.ing = []
        self.inglist = []
        self.steps = []
        self.time = {}
        self.style = ''
        self.tools = []
        self.methods = []

    def tomongo(self):
        item = {'_id': hash(self.url + self.name) & 0xffffffff,
                'url': self.url,
                'name': self.name,
                'ingredients': self.ing,
                'inglist': self.inglist,
                'steps': self.steps,
                'time': self.time,
                'style': self.style,
                'tools': self.tools,
                'methods': self.methods}
        return item

    def __str__(self):
        if not self.id:
            self.id = hash(self.url + self.name) & 0xffffffff
        result = 'id: {0}\nname: {1}\nurl: {2}\n'.format(self.id, self.name, self.url)
        step = '#'.join(self.steps)
        step = step.replace('{i', '{').format(*self.inglist)
        step = step.replace('{t', '{').format(*self.tools)
        step = step.replace('{m', '{').format(*self.methods)
        result += '\n'.join(step.split('#'))
        return result

    def feed(self):
        self.feedToolAndAction()
        self.feedStyle()
        self.formatSteps()

    def feedToolAndAction(self):
        toollist = Trie.getTrieByName('tools')
        methodlist = Trie.getTrieByName('actions')
        for step in self.steps:
            words = nltk.word_tokenize(step)
            bigram = nltk.bigrams(words)
            for word in words:
                match = word.strip().lower()
                if match in toollist:
                    self.tools.append(word)
                if match in methodlist:
                    self.methods.append(word)
            for pair in bigram:
                phrase = ' '.join(pair)
                match = phrase.lower()
                if toollist.byPrefix(match):
                    self.tools.append(phrase)
                if methodlist.byPrefix(match):
                    self.methods.append(phrase)
        self.tools = list(set(self.tools))
        self.methods = list(set(self.methods))

    def feedStyle(self):
        mongo = MongoJuice('recipes', 'styles')
        styles = ['American', 'Italian', 'Asian', 'Mexican']
        counter = Counter({x: 0 for x in styles})
        for ing in self.inglist:
            for style in styles:
                if mongo.likefindone(style, ing.lower()):
                    counter[style] += 1
        self.style = counter.most_common(1)[0][0]

    def formatSteps(self):
        for i in range(len(self.steps)):
            self.steps[i] = self._replaceKeyword(self.steps[i], self.inglist, 'i')
            self.steps[i] = self._replaceKeyword(self.steps[i], self.tools, 't')
            self.steps[i] = self._replaceKeyword(self.steps[i], self.methods, 'm')
        optinglist = self._reParseIng()
        for i in range(len(self.steps)):
            for item in optinglist:
                self.steps[i] = self.steps[i].replace(item[0], '{i'+str(item[1])+'}')
        self._removeDuplicatIng(2)

    def _replaceKeyword(self, s, l, c):
        f = 1
        if c == 't':
            f = 2
        elif c == 'm':
            f = 4
        for i, item in enumerate(l):
            s = s.replace(item, '{'*f+c+str(i)+'}'*f)
        return s

    def _reParseIng(self):
        result = []
        specialcase = ['with', 'ing', 'and', 'the', 'let', 'hot', 'per', 'cool']
        for step in self.steps:
            words = nltk.word_tokenize(step)
            bigram = nltk.bigrams(words)
            for word in words:
                if len(word) > 2 and word not in specialcase:
                    for i, ing in enumerate(self.inglist):
                        ing = ing.lower()
                        if word.lower() in ing:
                            result.append((word, i))
            for pair in bigram:
                phrase = ' '.join(pair)
                for i, ing in enumerate(self.inglist):
                    if phrase.lower() in ing.lower():
                        result.append((phrase, i))
        result = list(set(result))
        result.sort(cmp=lambda x, y: cmp(len(y[0]), len(x[0])))
        return result

    def _removeDuplicatIng(self, limit):
        if limit < 2:
            raise ValueError('Limit must greater than 1.')
        for i in range(len(self.steps)):
            for j in range(len(self.inglist)):
                bean = '{i'+str(j)+'}'
                for k in range(limit, 1, -1):
                    self.steps[i] = self.steps[i].replace(' '.join([bean]*k), bean)