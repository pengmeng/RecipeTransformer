__author__ = 'mengpeng'
import urllib
import os
from handler import RecipeHandler
from handler import LinkHandler
from transformer.util.tools import gethash


class Scraper(object):

    def __init__(self, debug=False, spidermode=False, tmpfile=True):
        self.debug = debug
        self.spidermode = spidermode
        self.tmpfile = tmpfile

    def exists(self, url):
        filename = self._tmpfilename(url)
        return os.path.exists(filename)

    def fetchone(self, url, *handlers):
        result = self.fetch([url], *handlers)
        return result and result[gethash(url)]

    def fetch(self, urllist, *handlers):
        results = {}
        for url in iter(urllist):
            if self.exists(url):
                if not self.spidermode:
                    html = self._loadfile(url)
                    if self.debug:
                        print('Load {0}.html from file.'.format(gethash(url)))
                else:
                    if self.debug:
                        print('{0}.html already visited.'.format(gethash(url)))
                    continue
            else:
                html = self._download(url)
                if self.tmpfile:
                    self._save2file(url, html)
                    if self.debug:
                        print('Download {0} and save as {1}.html'.format(url, gethash(url)))
            result = []
            for handler in iter(handlers):
                result.append(handler.parse(html, url))
            results[gethash(url)] = result
        return results

    def _download(self, url):
        html = urllib.urlopen(url).read()
        return html

    def _loadfile(self, url):
        filename = self._tmpfilename(url)
        with open(filename, 'r') as infile:
            content = infile.read()
        return content

    def _save2file(self, url, content):
        filename = self._tmpfilename(url)
        with open(filename, 'w') as outfile:
            outfile.write(content)
            outfile.flush()

    def _tmpfilename(self, url):
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')
        return './tmp/' + str(gethash(url)) + '.html'

if __name__ == '__main__':
    urls = ['http://allrecipes.com/Recipe/Baked-Coconut-Shrimp/Detail.aspx',
            'http://allrecipes.com/Recipe/Pork-Chops-with-Apple-Cider-Glaze/Detail.aspx',
            'http://allrecipes.com/Recipe/Butter-Roasted-Cauliflower/Detail.aspx',
            'http://allrecipes.com/Recipe/Zucchini-Yogurt-Multigrain-Muffins/Detail.aspx',
            'http://allrecipes.com/Recipe/Easy-Corned-Beef-and-Cabbage/Detail.aspx']
    hd = RecipeHandler()
    hd2 = LinkHandler()
    sp = Scraper(True)
    # r1 = sp.fetch(urls, hd)
    r2 = sp.fetchone('http://allrecipes.com/Recipe/Brussels-Sprouts-Slaw-with-Honey-Yogurt-Dressing/Detail.aspx', hd)
    print(r2[0].ing)