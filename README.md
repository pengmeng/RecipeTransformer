RecipeTransformer
========================

Project 2 for EECS337@Northwestern U

Build
------------------------
Please do following steps before running any program.
### Install packages
Please make sure you have gcc or other compilers installed on your machine
``` shell
> pip install -r requirement.txt
```

### Build MongoDB
A database named 'recipes' will be created.
``` shell
> sh buildmongo.sh
```

How To
------------------------
### Run web app
Web app will run on http://localhost:5000
``` shell
> python webapp.py
```

### Run spider.py
spider.py is a web crawler program for collecting recipes
- Download urls
``` shell
> python spider.py url1 url2 ...
```
- Start crawler with an url
``` shell
> python spider.py start url
```
- Search with a keyword
``` shell
> python spider.py search keyword
```

Authors
------------------------
Shiv Chandra Kumar, Marc Malinowski, Chris Dayal, Peng Meng

Third Party Libraries
------------------------
- [beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/)
- [pymongo](http://www.mongodb.org)
- [marisa-trie](https://github.com/kmike/marisa-trie)
- [nltk](http://www.nltk.org)
- [Flask](http://flask.pocoo.org)

ToDo
------------------------
- [x] Refactor Scraper to support handlers sequence
- [x] Persist spider frontier in mongo or file
- [x] Implement Converter
- [x] Add search support for spider
- [x] Add Flask UI
- [x] Update MongoJuice to optimize insert
- [x] Parse serving # and add serving transformation
