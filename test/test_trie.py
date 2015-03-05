__author__ = 'mengpeng'
from unittest import TestCase
from recipe.trie import Trie


class TestTrie(TestCase):
    def test_getTrieByName(self):
        self.assertRaises(AttributeError, Trie.getTrieByName, 'unknown')
        self.assertEqual(79, Trie.getTrieByName('actions').count())

    def test_triedict(self):
        Trie.getTrieByName('actions')
        self.assertTrue('actions' in Trie.TrieDict)
        self.assertTrue('fruits' not in Trie.TrieDict)
        self.assertTrue(79, Trie.TrieDict['actions'].count())

    def test_in(self):
        trie = Trie.getTrieByName('actions')
        self.assertFalse('adddd' in trie)
        self.assertTrue('bake' in trie)

    def test_prefixesOf(self):
        trie = Trie.getTrieByName('actions')
        self.assertEqual(2, len(trie.prefixesOf('sautee')))
        self.assertIsNone(trie.prefixesOf('notexists'))

    def test_byPrefix(self):
        trie = Trie.getTrieByName('actions')
        self.assertEqual(4, len(trie.byPrefix('br')))
        self.assertIsNone(trie.byPrefix('notexists'))