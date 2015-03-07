__author__ = 'mengpeng'
from bs4 import BeautifulSoup
from transformer.recipe import Recipe


class Handler(object):

    def __init__(self):
        pass

    def parse(self, html, url):
        raise NotImplementedError


class LinkHandler(Handler):

    def __init__(self):
        super(LinkHandler, self).__init__()

    def parse(self, html, url):
        bs = BeautifulSoup(html)
        prefix, suffix = '/Recipe/', 'Detail.aspx'
        result = []
        for link in bs.find_all('a', href=True):
            href = link.get('href')
            if href and prefix in href and suffix in href:
                href = href[href.index(prefix):href.index(suffix)+len(suffix)]
                href = 'http://allrecipes.com' + href
                result.append(href)
        result = list(set(result))
        return result


class RecipeHandler(Handler):

    def __init__(self):
        super(RecipeHandler, self).__init__()
        self.bs = None

    def parse(self, html, url):
        recipe = Recipe()
        recipe.url = url
        self.bs = BeautifulSoup(html)
        recipe.name = self.bs.find('h1', id='itemTitle', itemprop='name').string
        self.parseInteg(recipe)
        self.parseSteps(recipe)
        self.parseTime(recipe)
        return recipe

    def parseInteg(self, recipe):
        ingredients = self.bs('li', {'id': 'liIngredient'})
        for i in xrange(len(ingredients)):
            each, newing = ingredients[i], {'id': i}
            try:
                amountstr = each.find('span', {'class': 'ingredient-amount'}).string
            except AttributeError:
                newing['quantity'] = ''
                newing['measurement'] = ''
            else:
                if '(' in amountstr:
                    amountstr = amountstr[amountstr.index('(')+1:amountstr.index(')')]
                amount = amountstr.split(' ')
                newing['quantity'] = ' '.join(amount[:-1])
                newing['measurement'] = amount[-1]
            name = each.find('span', {'class': 'ingredient-name'}).string
            if 'to taste' in name and not newing['quantity']:
                newing['quantity'] = 'to taste'
                name = name.replace(' to taste', '')
            if ',' in name:
                name = name.split(',')
                newing['name'] = name[0]
                newing['description'] = ', '.join(name[1:])
                recipe.inglist.append(name[0])
            else:
                newing['name'] = name
                newing['description'] = ''
                recipe.inglist.append(name)
            recipe.ing.append(newing)

    def parseSteps(self, recipe, replaceIng=False):
        steps = self.bs.find('div', {'class': 'directions'}).find('ol')
        steps = steps('li')
        for each in iter(steps):
            step = each.find('span').string
            if replaceIng:
                for i in xrange(len(recipe.inglist)):
                    item = recipe.inglist[i]
                    if item in step:
                        step = step.replace(item, '{'+str(i)+'}')
            recipe.steps.append(step)

    def parseTime(self, recipe):
        recipe.time['prep'] = self.parseTimeFormat('prep')
        recipe.time['cook'] = self.parseTimeFormat('cook')
        recipe.time['total'] = self.parseTimeFormat('total')

    def parseTimeFormat(self, key):
        times = self.bs.find('div', {'class': 'right-aside preptime'}).find('ul')
        mins = times.find('span', {'id': key + 'MinsSpan'})
        hrs = times.find('span', {'id': key + 'HoursSpan'})
        days = times.find('span', {'id': key + 'DaysSpan'})
        timestr = ''
        if days:
            timestr += days.find('em').string + ' days '
        if hrs:
            timestr += hrs.find('em').string + ' hours '
        if mins:
            timestr += mins.find('em').string + ' mins'
        return timestr