__author__ = 'mengpeng'
import unittest
from unittest import TestCase
from transformer.converter import Converter
from transformer.recipe import Recipe
from transformer.util.mongo_juice import MongoJuice


class TestConverter(TestCase):
    def setUp(self):
        mongo = MongoJuice('recipes', 'recipe')
        self.old = Recipe.frommongo(mongo.likefindone('style', 'American'))
        self.converter = Converter(self.old)

    @unittest.skip('')
    def test__convertStyles(self):
        print(self.old.inglist)
        stylelist = ['American', 'Asian', 'Mexican', 'Italian']
        mongo = MongoJuice('recipes', 'recipe')
        old = Recipe.frommongo(mongo.likefindone('style', 'Italian'))
        new = self.converter._convertStyles(stylelist[(stylelist.index(old.style) + 1) % 4])
        print(new.inglist)
        new = self.converter._convertStyles(stylelist[(stylelist.index(new.style) + 1) % 4])
        print(old.inglist)
        print(new.inglist)

    @unittest.skip('')
    def test__convertPrefer(self):
        print(self.old.inglist)
        new = self.converter.convertTo('vegan')
        print(new.inglist)

    @unittest.skip('')
    def test__convertLactose(self):
        print(self.old.inglist)
        new = self.converter.convertTo('lactose-free')
        print(new.inglist)