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

    @unittest.skip('')
    def test_formatSteps(self):
        s = Scraper(True)
        h = RecipeHandler()
        recipe = s.fetchone('http://allrecipes.com/Recipe/Vegan-Red-Lentil-Soup/Detail.aspx', h)
        recipe.feed()
        print(recipe.name)
        for each in recipe.steps:
            print(each)

    @unittest.skip('')
    def test_str(self):
        s = Scraper(True)
        h = RecipeHandler()
        recipe = s.fetchone('http://allrecipes.com/Recipe/Vegan-Red-Lentil-Soup/Detail.aspx', h)
        recipe.feed()
        print(recipe)

    def test_feedIngList(self):
        s = Scraper(True)
        h = RecipeHandler()
        recipe = s.fetchone('http://allrecipes.com/Recipe/Vegan-Red-Lentil-Soup/Detail.aspx', h)
        recipe.feedIngList()
        print(recipe.ing)
        print(recipe.inglist)