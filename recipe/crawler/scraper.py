__author__ = 'mengpeng'
import urllib
import os
from handler import RecipeHandler


class Scraper(object):

    def __init__(self, urls, handler=None):
        self._urls = urls
        self._handler = handler

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, value):
        self._urls = value

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, value):
        self._handler = value

    def fetch(self):
        result = {}
        for url in self._urls:
            html = urllib.urlopen(url).read()
            self._save2file(url, html)
            result[url] = self._handler.parse(html, url)
        return result

    def _save2file(self, url, content):
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')
        filename = "./tmp/" + str(hash(url) & 0xffffffff) + ".html"
        with open(filename, 'w') as outfile:
            outfile.write(content)
            outfile.flush()

if __name__ == '__main__':
    urls = ["http://allrecipes.com/Recipe/Baked-Coconut-Shrimp/Detail.aspx",
            'http://allrecipes.com/Recipe/Pork-Chops-with-Apple-Cider-Glaze/Detail.aspx',
            'http://allrecipes.com/Recipe/Butter-Roasted-Cauliflower/Detail.aspx',
            'http://allrecipes.com/Recipe/Zucchini-Yogurt-Multigrain-Muffins/Detail.aspx',
            'http://allrecipes.com/Recipe/Easy-Corned-Beef-and-Cabbage/Detail.aspx']
    hd = RecipeHandler()
    sp = Scraper(urls, hd)
    r = sp.fetch()
    print(r[urls[4]].time)
    # print(r[urls[1]].ing)
    # print(r[urls[2]].ing)
    # print(r[urls[3]].ing)