__author__ = 'mengpeng'
from unittest import TestCase
from recipe.util.mongo_juice import MongoJuice


class TestMongoJuice(TestCase):
    def test_config(self):
        MongoJuice.config({'host': 'localhost', 'port': 27017})
        self.assertEqual('localhost', MongoJuice.Host)
        self.assertEqual(27017, MongoJuice.Port)

    def test_insert(self):
        mongo = MongoJuice('recipes', 'test')
        self.assertRaises(TypeError, mongo.insert, [1])
        #mongo.insert({'test': 'insert', 'value': 2})
        # self.assertEqual(3, mongo.count())