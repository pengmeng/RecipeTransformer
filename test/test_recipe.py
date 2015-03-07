__author__ = 'mengpeng'
import unittest
from unittest import TestCase
from transformer.crawler.scraper import Scraper
from transformer.crawler.handler import RecipeHandler


class TestRecipe(TestCase):
    @unittest.skip('')
    def test_feedTools(self):
        s = Scraper(True)
        h = RecipeHandler()
        recipe = s.fetchone('http://allrecipes.com/Recipe/Easy-Corned-Beef-and-Cabbage/Detail.aspx', h)
        recipe.feedToolAndAction()
        print(recipe.name)
        print(recipe.inglist)
        for each in recipe.steps:
            print(each)
        print(recipe.tools)
        print(recipe.methods)

    @unittest.skip('')
    def test_feedStyle(self):
        s = Scraper(True)
        h = RecipeHandler()
        recipe = s.fetchone('http://allrecipes.com/Recipe/Baked-Coconut-Shrimp/Detail.aspx', h)
        recipe.feedToolAndAction()
        recipe.feedStyle()
        print(recipe.name)
        print(recipe.style)