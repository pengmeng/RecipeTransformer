__author__ = 'mengpeng'
import os
import marisa_trie


class Trie(object):

    TrieDict = {}

    def __init__(self, trie=None, name=''):
        self.trie = trie
        self.name = name

    @staticmethod
    def getTrieByName(name, bytestrie=False):
        if name in Trie.TrieDict:
            return Trie.TrieDict[name]
        filename = './marisa/' + name + '.marisa'
        if not os.path.exists(filename):
            raise AttributeError('{0} is not found in marisa models.'.format(filename))
        trie = marisa_trie.Trie() if not bytestrie else marisa_trie.BytesTrie()
        trie.load(filename)
        mytrie = Trie(trie, name)
        Trie.TrieDict[name] = mytrie
        return mytrie

    def __len__(self):
        return len(self.trie)

    def __contains__(self, item):
        return unicode(item) in self.trie

    def prefixesOf(self, item):
        result = self.trie.prefixes(unicode(item.lower()))
        return map(str, result)

    def byPrefix(self, prefix):
        result = self.trie.keys(unicode(prefix.lower()))
        return map(str, result)

    def items(self):
        return iter(self.trie.items())