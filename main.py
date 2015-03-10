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
    # hd = RecipeHandler()
    # sp = Scraper(True, True)
    # result = sp.fetch(urls, RecipeHandler(), LinkHandler())
    # if result:
    #     for key, value in result.iteritems():
    #         print(key)
    #         if len(value) == 2 and value[1]:
    #             for each in value[1]:
    #                 print(each)
    mongo = MongoJuice('recipes', 'recipe')
    results = mongo.find()
    for each in results:
        if '' in each['inglist']:
            print(each['inglist'])
