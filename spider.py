__author__ = 'mengpeng'
import sys
import urllib
from transformer.util.mongo_juice import MongoJuice
from transformer.util.tools import gethash
from transformer.util.tools import timestamp
from transformer.crawler.scraper import Scraper
from transformer.crawler.handler import LinkHandler
from transformer.crawler.handler import RecipeHandler


def forgrader(url):
    scraper = Scraper(True)
    result = scraper.fetchone(url, RecipeHandler())
    if result:
        recipe = result[0]
        recipe.feed()
        return tograderforamt(recipe)
    raise Warning('No result from ' + url)


def tograderforamt(recipe):
    result = {'url': recipe.url, 'ingredients': []}
    for ing in iter(recipe.ing):
        item = {}
        item['name'] = [str(ing['name'])]
        item['quantity'] = [ing['quantity']]
        item['measurement'] = [ing['measurement']]
        item['descriptor'] = [x.lower() for x in map(str, ing['description'])]
        item['preparation'] = [x.lower() for x in map(str, ing['preparation'])]
        item['prep-description'] = ''
        result['ingredients'].append(item)
    result['cooking tools'] = [x.lower() for x in map(str, recipe.tools)]
    result['cooking methods'] = [x.lower() for x in map(str, recipe.methods)]
    result['primary cooking method'] = ''
    return result


def getone(urls):
    mongo = MongoJuice('recipes', 'recipe')
    scraper = Scraper(True, True)
    for url in iter(urls):
        result = scraper.fetchone(url, RecipeHandler())
        if result:
            recipe = result[0]
            recipe.feed()
            mongo.insert(recipe.tomongo())
            print('{0} is inserted into mongodb.'.format(recipe.id))


def start(url):
    mongo = MongoJuice('recipes', 'recipe')
    todo = MongoJuice('recipes', 'todo')
    scraper = Scraper(True, True, False)
    result = scraper.fetchone(url, LinkHandler())
    flag = True
    if result:
        frontier = result[0]
    else:
        frontier = []
        print('No valid url found in {0}'.format(url))
        print('Will start from todo urls in databases.')
    while flag:
        try:
            if not frontier:
                if todo.count() == 0:
                    print('No urls in databases.')
                    break
                items = todo.find(limit=20)
                for each in items:
                    if not scraper.exists(each['url']):
                        frontier.append(each['url'])
                    todo.remove(each['_id'])
            if not frontier:
                continue
            scraper.tmpfile = True
            results = scraper.fetch(frontier, RecipeHandler(), LinkHandler())
            frontier = []
            if results:
                for result in results.itervalues():
                    if result[0]:
                        recipe = result[0]
                        recipe.feed()
                        mongo.insert(recipe.tomongo())
                        print('{0} is inserted into mongodb.'.format(recipe.id))
                    if result[1]:
                        for each in iter(result[1]):
                            if not scraper.exists(each):
                                todo.insert({'_id': gethash(each), 'url': each})
        except KeyboardInterrupt:
            if frontier:
                for each in iter(frontier):
                    if not scraper.exists(each):
                        todo.insert({'_id': gethash(each), 'url': each})
            flag = False
            print('{0} todo urls are inserted in database'.format(len(frontier)))
            print('KeyboardInterrupt. Spider will stop.')
        except Exception as error:
            with open('exception.log', 'a') as logfile:
                logfile.write(timestamp() + ' ' + error.message + '\n')
    else:
        print('Exiting.')


def search(keyword):
    url = 'http://allrecipes.com/search/default.aspx?'
    url += urllib.urlencode({'wt': keyword})
    mongo = MongoJuice('recipes', 'recipe')
    scraper = Scraper(True, True, False)
    urls = scraper.fetchone(url, LinkHandler())
    if not urls:
        print('No valid urls found in {0}'.format(url))
    else:
        frontier = urls[0][:min(5, len(urls[0]))]
        scraper.tmpfile = True
        results = scraper.fetch(frontier, RecipeHandler())
        if results:
            for result in results.itervalues():
                recipe = result[0]
                recipe.feed()
                mongo.insert(recipe.tomongo())
                print('{0} is inserted into mongodb.'.format(recipe.id))


def printhelp():
    print('Missing argument or command. Using as following:')
    print('To scrape urls:')
    print('python spider.py [url ...]')
    print('To start:')
    print('python spider.py start [seed url]')
    print('To search:')
    print('python spider.py search [keyword]')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'start':
            if len(sys.argv) != 3:
                print('start command needs a seed url.')
            else:
                start(sys.argv[2])
        elif sys.argv[1] == 'search':
            if len(sys.argv) != 3:
                print('search command needs a keyword.')
            else:
                search(sys.argv[2])
        else:
            getone(sys.argv[1:])
    else:
        printhelp()
