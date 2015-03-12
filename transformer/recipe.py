__author__ = 'mengpeng'
import nltk
import string
from trie import Trie
from util.mongo_juice import MongoJuice
from util.tools import gethash
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
    
    @staticmethod
    def frommongo(item):
        recipe = Recipe()
        recipe.id = item['_id']
        recipe.url = item['url']
        recipe.name = item['name']
        recipe.ing = item['ingredients']
        recipe.inglist = item['inglist']
        recipe.steps = item['steps']
        recipe.time = item['time']
        recipe.style = item['style']
        recipe.tools = item['tools']
        recipe.methods = item['methods']
        return recipe

    def tomongo(self):
        item = {'_id': gethash(self.url + self.name),
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
            self.id = gethash(self.url + self.name)
        result = 'id: {0}\nname: {1}\nurl: {2}\n'.format(self.id, self.name, self.url)
        step = '#'.join(self.steps)
        step = step.replace('{i', '{').format(*self.inglist)
        step = step.replace('{t', '{').format(*self.tools)
        step = step.replace('{m', '{').format(*self.methods)
        result += '\n'.join(step.split('#'))
        return result

    def feed(self):
        self.id = gethash(self.url + self.name)
        self.feedIngList()
        self.feedToolAndAction()
        self.feedStyle()
        self.formatSteps()

    def feedIngList(self):
        desclist = Trie.getTrieByName('descriptors')
        preplist = Trie.getTrieByName('preparation')
        special = ['and', 'until', 'into']
        for each in iter(self.ing):
            name = each['name'].lower()
            each['description'], each['preparation'] = [], []
            name = ''.join([c for c in name if c not in string.punctuation])
            tokens, after = name.split(' '), []
            for token in iter(tokens):
                if token in desclist:
                    each['description'].append(token)
                elif token in preplist:
                    each['preparation'].append(token)
                elif token not in special and token != '':
                    after.append(token)
            name = ' '.join(after)
            if 'to taste' in name:
                each['quantity'] = str(each['quantity'])
                each['quantity'] += 'to taste' if each['quantity'] == '' else ' or to taste'
                name = name.replace(' to taste', '')
            each['name'] = name.strip()
            self.inglist.append(name)

    def feedToolAndAction(self):
        toollist = Trie.getTrieByName('tools')
        methodlist = Trie.getTrieByName('actions')
        for step in iter(self.steps):
            words = nltk.word_tokenize(step)
            bigram = nltk.bigrams(words)
            for word in iter(words):
                match = word.strip().lower()
                if match in toollist:
                    self.tools.append(word)
                if match in methodlist:
                    self.methods.append(word)
            for pair in iter(bigram):
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
        for ing in iter(self.inglist):
            for style in styles:
                if mongo.likefindone(style, ing.lower()):
                    counter[style] += 1
        self.style = counter.most_common(1)[0][0]

    def formatSteps(self):
        for i in xrange(len(self.steps)):
            self.steps[i] = self._replaceKeyword(self.steps[i], self.inglist, 'i')
            self.steps[i] = self._replaceKeyword(self.steps[i], self.tools, 't')
            self.steps[i] = self._replaceKeyword(self.steps[i], self.methods, 'm')
        optinglist = self._reParseIng()
        for i in xrange(len(self.steps)):
            for item in iter(optinglist):
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
        for step in iter(self.steps):
            words = nltk.word_tokenize(step)
            bigram = nltk.bigrams(words)
            for word in iter(words):
                if len(word) > 2 and word not in specialcase:
                    for i, ing in enumerate(self.inglist):
                        ing = ing.lower()
                        if word.lower() in ing:
                            result.append((word, i))
            for pair in iter(bigram):
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
        for i in xrange(len(self.steps)):
            for j in xrange(len(self.inglist)):
                bean = '{i'+str(j)+'}'
                for k in xrange(limit, 1, -1):
                    self.steps[i] = self.steps[i].replace(' '.join([bean]*k), bean)
                    self.steps[i] = self.steps[i].replace(' and '.join([bean]*k), bean)

    def ingStr(self):
        result = []
        for each in self.ing:
            s = '{0} {1}'.format(each['quantity'], each['measurement'])
            if each['description']:
                s += ', ' + str(map(str, each['description']))
            s += ', ' + each['name']
            if each['preparation']:
                s += ', ' + str(map(str, each['preparation']))
            result.append(s)
        return result

    def stepStr(self):
        step = '#'.join(self.steps)
        step = step.replace('{i', '{').format(*self.inglist)
        step = step.replace('{t', '{').format(*self.tools)
        step = step.replace('{m', '{').format(*self.methods)
        return step.split('#')

    def toolStr(self):
        return str(map(str, self.tools))

    def methodStr(self):
        return str(map(str, self.methods))