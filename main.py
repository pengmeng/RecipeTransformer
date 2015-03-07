__author__ = 'mengpeng'
from transformer.crawler.scraper import Scraper
from transformer.crawler.handler import RecipeHandler
from transformer.crawler.handler import LinkHandler
from transformer.util.mongo_juice import MongoJuice


if __name__ == '__main__':
    urls = ['http://allrecipes.com/Recipe/Baked-Coconut-Shrimp/Detail.aspx',
            'http://allrecipes.com/Recipe/Pork-Chops-with-Apple-Cider-Glaze/Detail.aspx',
            'http://allrecipes.com/Recipe/Butter-Roasted-Cauliflower/Detail.aspx',
            'http://allrecipes.com/Recipe/Zucchini-Yogurt-Multigrain-Muffins/Detail.aspx',
            'http://allrecipes.com/Recipe/Easy-Corned-Beef-and-Cabbage/Detail.aspx',
            'http://allrecipes.com/Recipe/Lentils-and-Rice-with-Fried-Onions-Mujadarrah/Detail.aspx',
            'http://allrecipes.com/Recipe/Red-Lentil-Curry/Detail.aspx',
            'http://allrecipes.com/Recipe/Red-Lentil-Burgers/Detail.aspx',
            'http://allrecipes.com/Recipe/Vegan-Red-Lentil-Soup/Detail.aspx']
    hd = RecipeHandler()
    sp = Scraper(True, True)
    result = sp.fetch(urls, RecipeHandler(), LinkHandler())
    if result:
        for key, value in result[1].iteritems():
            print(key)
            for item in value:
                print(item)

    #results contains recipe objects
    #get each recipe by their url
    # recipe = result[urls[0]]
    # print(recipe.name)

    # #Follwing example show how to get knowledge base
    # #all knowledge base are in transformer/marisa/
    # actions = Trie.getTrieByName('actions')
    # #try to find whether an action is in list
    # if 'bake' in actions:
    #     #get all match items with prefix 'bake'
    #     print(actions.byPrefix('bake'))
    # if 'something' not in actions:
    #     print('something is not in actions')
    # #get the list of proteins
    # proteins = Trie.getTrieByName('proteins')
    # #get all item with prefix 'European'
    # print(proteins.byPrefix('European'))