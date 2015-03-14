RecipeTransformer
========================

Project 2 for EECS337@Northwestern U

How To
------------------------
### Install packages
``` shell
> pip install -r requirement.txt
```

### Build MongoDB
``` shell
> sh buildmongo.sh
```

### Run web app
Web app will run on http://localhost:5000
``` shell
> python webgui.py
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
- [ ] Parse serving # and add serving transformation
