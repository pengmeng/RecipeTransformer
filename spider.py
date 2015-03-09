__author__ = 'mengpeng'
import sys
from transformer.util.mongo_juice import MongoJuice
from transformer.util.tools import timestamp
from transformer.crawler.scraper import Scraper
from transformer.crawler.handler import LinkHandler
from transformer.crawler.handler import RecipeHandler


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
    elif len(sys.argv) == 3 and sys.argv[1] == 'search':
        pass
    else:
        # url = 'http://allrecipes.com/'
        url = 'http://allrecipes.com/Recipe/Watermelon-Salsa/Detail.aspx'
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
                            if len(frontier) >= 100:
                                del result[1]
                                break
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
                    logfile.write(timestamp() + ' ' + error.message + '\n')
        else:
            print('Exiting.')