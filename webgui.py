__author__ = 'mengpeng'
from flask import Flask
from flask import render_template
from flask import request
from urllib2 import unquote
from urllib import urlencode
from transformer.crawler.handler import RecipeHandler
from transformer.crawler.handler import LinkHandler
from transformer.crawler.scraper import Scraper

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
            return render_template('display.html', title='Display', recipe=recipe)
    return render_template('display.html')


if __name__ == "__main__":
    app.run(debug=True)