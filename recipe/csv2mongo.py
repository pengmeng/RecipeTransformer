__author__ = 'mengpeng'
import sys
from util.mongo_juice import MongoJuice


def tomongo(filename, collname, skipfirt=False):
    mongo = MongoJuice('recipes', collname)
    with open(filename, 'r') as csvfile:
        if skipfirt:
            csvfile.readline()
        for line in csvfile:
            line = line.strip()
            line = line.split(',')
            item = {'American': line[0].strip(),
                    'Italian': line[1].strip(),
                    'Asian': line[2].strip(),
                    'Mexican': line[3].strip()}
            mongo.insert(item)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Missing argument. Use like this:')
        print('python csv2mongo.py csvfile collectionname')
    else:
        tomongo(sys.argv[1], sys.argv[2], True)