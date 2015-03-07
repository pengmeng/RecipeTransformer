__author__ = 'mengpeng'
import unittest
from unittest import TestCase
from transformer.crawler.scraper import Scraper
from transformer.crawler.handler import LinkHandler

@unittest.skip('')
class TestLinkHandler(TestCase):
    def test_parse(self):
        s = Scraper(True)
        h = LinkHandler()
        r = s.fetchone('http://allrecipes.com', h)
        print(len(r))
        for each in r:
            print(each)