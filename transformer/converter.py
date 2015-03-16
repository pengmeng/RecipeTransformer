__author__ = 'mengpeng'
from copy import deepcopy
from random import randint
from trie import Trie
from util.mongo_juice import MongoJuice

lists = {'vegetarian': ['tofu', 'mushroom', 'peppers', 'eggplant'],
         'vegan': ['tofu', 'mushroom', 'peppers', 'eggplant']}


class Converter(object):

    def __init__(self, recipe):
        self.oldrecipe = recipe
        self.newrecipe = None

    def convertTo(self, keyword):
        if keyword in ['American', 'Asian', 'Mexican', 'Italian']:
            new = self._convertStyles(keyword)
        elif keyword in ['vegetarian', 'vegan']:
            new = self._convertPrefer(keyword)
        elif keyword in ['low-calorie', 'low-fat', 'low-sodium', 'lactose-free']:
            new = self._convertHealthy(keyword)
        elif keyword.isdigit():
            new = self._convertServing(keyword)
        else:
            raise AttributeError('keyword {0} is unknown.'.format(keyword))
        return new

    def _convertStyles(self, keyword):
        mongo = MongoJuice('recipes', 'styles')
        recipe = self.newrecipe if self.newrecipe else deepcopy(self.oldrecipe)
        style = recipe.style
        for each in iter(recipe.ing):
            result = mongo.findone({style: each['name']})
            if result and result[keyword]:
                each['name'] = result[keyword]
                recipe.inglist[each['id']] = each['name']
        recipe.style = keyword
        self.newrecipe = recipe
        return self.newrecipe

    def _convertPrefer(self, keyword):
        array = lists[keyword]
        proteins = Trie.getTrieByName('proteins')
        recipe = self.newrecipe if self.newrecipe else deepcopy(self.oldrecipe)
        for ing in iter(recipe.ing):
            for key, value in proteins.items():
                if key in ing['name']:
                    ing['name'] = self._random(array)
                    recipe.inglist[ing['id']] = ing['name']
        self.newrecipe = recipe
        return self.newrecipe

    def _convertHealthy(self, keyword):
        healthy = Trie.getTrieByName(keyword, True)
        recipe = self.newrecipe if self.newrecipe else deepcopy(self.oldrecipe)
        for ing in iter(recipe.ing):
            for key, value in healthy.items():
                if key in ing['name']:
                    ing['name'] = value
                    recipe.inglist[ing['id']] = ing['name']
        self.newrecipe = recipe
        return self.newrecipe

    def _convertServing(self, serving):
        recipe = self.newrecipe if self.newrecipe else deepcopy(self.oldrecipe)
        factor = float(serving) / recipe.serving
        for ing in iter(recipe.ing):
            try:
                ing['quantity'] *= factor
            except (KeyError, TypeError):
                pass
        recipe.serving = serving
        self.newrecipe = recipe
        return recipe

    def _random(self, array):
        return array[randint(0, len(array) - 1)]
