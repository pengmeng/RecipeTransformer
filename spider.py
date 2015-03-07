__author__ = 'mengpeng'
import sys
import time
from transformer.util.mongo_juice import MongoJuice
from transformer.crawler.scraper import Scraper
from transformer.crawler.handler import LinkHandler
from transformer.crawler.handler import RecipeHandler


def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


if __name__ == '__main__':
    mongo = MongoJuice('recipes', 'recipe')
    scraper = Scraper(True, True)
    if len(sys.argv) == 2:
        url = sys.argv[1]
        recipe = scraper.fetchone(url, RecipeHandler())
        if recipe:
            recipe.feed()
            mongo.insert(recipe.tomongo())
            print('{0} is inserted into mongodb.'.format(recipe.id))
    else:
        url = 'http://allrecipes.com/'
        frontier, flag = scraper.fetchone(url, LinkHandler()), True
        while flag:
            try:
                while frontier:
                    result = scraper.fetch(frontier, RecipeHandler(), LinkHandler())
                    if result[0]:
                        for value in result[0].itervalues():
                            value.feed()
                            mongo.insert(value.tomongo())
                            print('{0} is inserted into mongodb.'.format(value.id))
                    if result[1]:
                        for value in result[1].itervalues():
                            frontier.extend(value)
            except KeyboardInterrupt:
                if frontier:
                    with open('frontier.txt', 'w+') as outfile:
                        outfile.write('\n'.join(frontier))
                flag = False
                print('{0} unvisited urls are stored in frontier.txt'.format(len(frontier)))
                print('KeyboardInterrupt. Spider will stop.')
            except Exception as error:
                with open('exception.log', 'w+') as logfile:
                    logfile.write(timestamp() + error.message + '\n')
        else:
            print('Exiting.')