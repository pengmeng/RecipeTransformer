__author__ = 'mengpeng'
import urllib
import os
from handler import RecipeHandler


class Scraper(object):

    def __init__(self, debug=False, spidermode=False):
        self.debug = debug
        self.spidermode = spidermode

    def exists(self, url):
        filename = self._tmpfilename(url)
        return os.path.exists(filename)

    def fetchone(self, url, handler):
        result = self._fetch([url], handler)
        return result and result[url]

    def fetch(self, urllist, *handlers):
        results = []
        for handler in handlers:
            result = self._fetch(urllist, handler)
            if result:
                results.append(result)
        if len(handlers) == 1:
            return results and results[0]
        else:
            return results

    def _fetch(self, urllist, handler):
        result = {}
        for url in iter(urllist):
            filename = self._tmpfilename(url)
            if os.path.exists(filename):
                if self.spidermode:
                    # continue
                    html = self._loadfile(filename)
                else:
                    html = self._loadfile(filename)
                    if self.debug:
                        print('Load {0} from file.'.format(filename))
            else:
                html = urllib.urlopen(url).read()
                self._save2file(filename, html)
                if self.debug:
                    print('Download {0} and save as {1}'.format(url, filename))
            result[url] = handler.parse(html, url)
        return result

    def _loadfile(self, filename):
        with open(filename, 'r') as infile:
            content = infile.read()
        return content

    def _save2file(self, filename, content):
        with open(filename, 'w') as outfile:
            outfile.write(content)
            outfile.flush()

    def _tmpfilename(self, url):
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')
        return './tmp/' + str(hash(url) & 0xffffffff) + '.html'

if __name__ == '__main__':
    urls = ['http://allrecipes.com/Recipe/Baked-Coconut-Shrimp/Detail.aspx',
            'http://allrecipes.com/Recipe/Pork-Chops-with-Apple-Cider-Glaze/Detail.aspx',
            'http://allrecipes.com/Recipe/Butter-Roasted-Cauliflower/Detail.aspx',
            'http://allrecipes.com/Recipe/Zucchini-Yogurt-Multigrain-Muffins/Detail.aspx',
            'http://allrecipes.com/Recipe/Easy-Corned-Beef-and-Cabbage/Detail.aspx']
    hd = RecipeHandler()
    sp = Scraper(True)
    r1 = sp.fetch(urls, hd)
    print(len(r1))
    r2 = sp.fetchone('http://allrecipes.com/Recipe/Amish-Meatloaf/Detail.aspx', hd)
    print(r2)
    # print(r[urls[4]].time)
    # print(r[urls[1]].ing)
    # print(r[urls[2]].ing)
    # print(r[urls[3]].ing)