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
        return 'id: {0} name: {1} url: {2}'.format(self.id, self.name, self.url)

    def feedToolAndAction(self):
        toollist = Trie.getTrieByName('tools')
        methodlist = Trie.getTrieByName('actions')
        for step in self.steps:
            words = nltk.word_tokenize(step)
            bigram = nltk.bigrams(words)
            for word in words:
                word = word.strip().lower()
                if word in toollist:
                    self.tools.append(word)
                if word in methodlist:
                    self.methods.append(word)
            for pair in bigram:
                phrase = ' '.join(pair)
                if toollist.byPrefix(phrase):
                    self.tools.append(phrase)
                if methodlist.byPrefix(phrase):
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