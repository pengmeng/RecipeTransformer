__author__ = 'mengpeng'


class Recipe(object):

    def __init__(self):
        self.id = ''
        self.url = ''
        self.name = ''
        self.ing = []
        self.inglist = []
        self.steps = []
        self.time = {}

    def tomongo(self):
        item = {'_id': hash(self.url + self.name) & 0xffffffff,
                'url': self.url,
                'name': self.name,
                'ingredients': self.ing,
                'inglist': self.inglist,
                'steps': self.steps,
                'time': self.time}
        return item

    def __str__(self):
        if not self.id:
            self.id = hash(self.url + self.name) & 0xffffffff
        return 'id: {0} name: {1} url: {2}'.format(self.id, self.name, self.url)