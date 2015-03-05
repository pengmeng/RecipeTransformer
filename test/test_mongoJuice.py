__author__ = 'mengpeng'
from unittest import TestCase
from recipe.util.mongo_juice import MongoJuice


class TestMongoJuice(TestCase):
    def test_config(self):
        MongoJuice.config({'host': 'localhost', 'port': 27017})
        self.assertEqual('localhost', MongoJuice.Host)
        self.assertEqual(27017, MongoJuice.Port)