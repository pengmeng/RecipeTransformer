__author__ = 'mengpeng'
import unittest
from unittest import TestCase
from transformer.util.mongo_juice import MongoJuice


class TestMongoJuice(TestCase):
    def test_config(self):
        MongoJuice.config({'host': 'localhost', 'port': 27017})
        self.assertEqual('localhost', MongoJuice.Host)
        self.assertEqual(27017, MongoJuice.Port)

    def test_insert(self):
        mongo = MongoJuice('recipes', 'test')
        item = mongo.findone()
        self.assertRaises(TypeError, mongo.insert, [1])
        self.assertRaises(AttributeError, mongo.insert, item, False)

    def test_likefindone(self):
        mongo = MongoJuice('recipes', 'test')
        self.assertTrue(mongo.likefindone('second', 'noo'))
        self.assertIsNone(mongo.likefindone('second', 'abdjedg'))

    def test_remove(self):
        mongo = MongoJuice('recipes', 'test')
        mongo.insert({'item': 'to be removed'})
        length = mongo.count()
        item = mongo.findone({'item': 'to be removed'})
        mongo.remove(item['_id'])
        self.assertEqual(length-1, mongo.count())

    def test_findone(self):
        mongo = MongoJuice('recipes', 'test')
        self.assertTrue(mongo.findone())