__author__ = 'mengpeng'
from flask import Flask
from flask import render_template
from flask import request
from urllib2 import unquote
from urllib import urlencode
from transformer.crawler.handler import RecipeHandler
from transformer.crawler.handler import LinkHandler
from transformer.crawler.scraper import Scraper
from transformer.util.mongo_juice import MongoJuice
from transformer.recipe import Recipe
from transformer.converter import Converter

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Search')


@app.route('/bykeyword', methods=['POST', 'GET'])
def bykeyword():
    if request.form['keyword']:
        url = 'http://allrecipes.com/search/default.aspx?'
        url += urlencode({'wt': request.form['keyword']})
        scraper = Scraper(True)
        scraper.tmpfile = False
        result = scraper.fetchone(url, LinkHandler())
        if result and result[0]:
            url = result[0][0]
            scraper.tmpfile = True
            result = scraper.fetchone(url, RecipeHandler())
            if result:
                recipe = result[0]
                recipe.feed()
                save2mongo(recipe)
                return render_template('display.html', title='Display', recipe=recipe)
    return render_template('display.html')


@app.route('/byurl', methods=['POST', 'GET'])
def byurl():
    if request.form['url']:
        scraper = Scraper(True)
        result = scraper.fetchone(unquote(request.form['url']), RecipeHandler())
        if result:
            recipe = result[0]
            recipe.feed()
            save2mongo(recipe)
            return render_template('display.html', title='Display', recipe=recipe)
    return render_template('display.html')


@app.route('/convert/<recipeid>', methods=['POST', 'GET'])
def convert(recipeid):
    recipe = frommongo(recipeid)
    if recipe:
        converter = Converter(recipe)
        if request.form['totype']:
            newrecipe = converter.convertTo(request.form['totype'])
            return render_template('display.html', title='Display', recipe=newrecipe)
    return render_template('display.html')


@app.route('/serving/<recipeid>', methods=['POST', 'GET'])
def serving(recipeid):
    recipe = frommongo(recipeid)
    if recipe:
        converter = Converter(recipe)
        if request.form['serving']:
            newrecipe = converter.convertTo(request.form['serving'])
            return render_template('display.html', title='Display', recipe=newrecipe)
    return render_template('display.html')


def save2mongo(recipe):
    mongo.insert(recipe.tomongo())


def frommongo(_id):
    result = mongo.findone({'_id': int(_id)})
    return result and Recipe.frommongo(result)

if __name__ == "__main__":
    mongo = MongoJuice('recipes', 'recipe')
    app.run(debug=True)