__author__ = 'mengpeng'
from transformer.util.mongo_juice import MongoJuice

if __name__ == '__main__':
    mongo = MongoJuice('recipes', 'recipe')
    result = mongo.find()
    for each in result:
        out = []
        print(each['_id'])
        for item in each['ingredients']:
            out.append(item['quantity'])
        print(out)