__author__ = 'mengpeng'

import pymongo


class MongoJuice(object):

    Host = 'localhost'
    Port = 27017
    Client = pymongo.MongoClient(Host, Port)

    @staticmethod
    def config(param):
        try:
            MongoJuice.Host = param['host']
            MongoJuice.Port = param['port']
        except KeyError:
            print('Unvalid configuration dict.')

    def __init__(self, db_name, coll_name):
        self.db_name = db_name
        self.coll_name = coll_name
        self._db = MongoJuice.Client[db_name]
        self._coll = self.db[coll_name]

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self.db_name = value
        self._db = MongoJuice.Client[self.db_name]

    @property
    def coll(self):
        return self._coll

    @coll.setter
    def coll(self, value):
        self.coll_name = value
        self._coll = self.db[value]

    def insert(self, items):
        if isinstance(items, dict):
            self._coll.insert(items)
        else:
            raise TypeError('Inserting item must be a dict.')

    def find(self, query=None, limit=0, sort=None, skip=0):
        return self._coll.find(spec=query, limit=limit, sort=sort, skip=skip)

    def count(self):
        return self._coll.count()