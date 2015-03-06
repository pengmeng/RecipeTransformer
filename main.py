__author__ = 'mengpeng'
from transformer.crawler.scraper import Scraper
from transformer.crawler.handler import RecipeHandler
from transformer.trie import Trie


if __name__ == '__main__':
    urls = ['http://allrecipes.com/Recipe/Baked-Coconut-Shrimp/Detail.aspx',
            'http://allrecipes.com/Recipe/Pork-Chops-with-Apple-Cider-Glaze/Detail.aspx',
            'http://allrecipes.com/Recipe/Butter-Roasted-Cauliflower/Detail.aspx',
            'http://allrecipes.com/Recipe/Zucchini-Yogurt-Multigrain-Muffins/Detail.aspx',
            'http://allrecipes.com/Recipe/Easy-Corned-Beef-and-Cabbage/Detail.aspx']
    hd = RecipeHandler()
    sp = Scraper(True)
    result = sp.fetch(urls, hd)
    #results contains recipe objects
    #get each recipe by their url
    recipe = result[urls[0]]
    print(recipe.name)

    #Follwing example show how to get knowledge base
    #all knowledge base are in transformer/marisa/
    actions = Trie.getTrieByName('actions')
    #try to find whether an action is in list
    if 'bake' in actions:
        #get all match items with prefix 'bake'
        print(actions.byPrefix('bake'))
    #get the list of proteins
    proteins = Trie.getTrieByName('proteins')
    #get all item with prefix 'European'
    print(proteins.byPrefix('European'))