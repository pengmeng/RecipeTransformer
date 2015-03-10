__author__ = 'mengpeng'
from unittest import TestCase
from transformer.crawler.handler import RecipeHandler


class TestRecipeHandler(TestCase):

    def test_parseFloat(self):
        h = RecipeHandler()
        self.assertEqual(1.0, h.parseFloat('1'))
        self.assertEqual(0.25, h.parseFloat('1/4'))
        self.assertEqual(0.67, h.parseFloat('2/3'))
        self.assertEqual(1.25, h.parseFloat('1 1/4'))
        self.assertEqual(0.33, h.parseFloat('1/3'))
        self.assertEqual('a', h.parseFloat('a'))
        self.assertEqual('a a', h.parseFloat('a a'))
        self.assertEqual('', h.parseFloat(''))