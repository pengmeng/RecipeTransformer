__author__ = 'mengpeng'
import unittest
from unittest import TestCase
from transformer.trie import Trie

@unittest.skip('succ')
class TestTrie(TestCase):
    def test_getTrieByName(self):
        self.assertRaises(AttributeError, Trie.getTrieByName, 'unknown')
        self.assertEqual(79, len(Trie.getTrieByName('actions')))

    def test_triedict(self):
        Trie.getTrieByName('actions')
        self.assertTrue('actions' in Trie.TrieDict)
        self.assertTrue('fruits' not in Trie.TrieDict)
        self.assertTrue(79, len(Trie.TrieDict['actions']))

    def test_in(self):
        trie = Trie.getTrieByName('actions')
        self.assertFalse('adddd' in trie)
        self.assertTrue('bake' in trie)

    def test_prefixesOf(self):
        trie = Trie.getTrieByName('actions')
        self.assertEqual(2, len(trie.prefixesOf('sautee')))
        self.assertFalse(trie.prefixesOf('notexists'))

    def test_byPrefix(self):
        trie = Trie.getTrieByName('actions')
        self.assertEqual(4, len(trie.byPrefix('br')))
        self.assertFalse(trie.byPrefix('notexists'))