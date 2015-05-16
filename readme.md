#Carboy

Carboy, a sister of the [Alva ideablog](https://github.com/tommeagher/alva), is a nanoblog application built using the Flask Python framework. Because who really needs another Tumblr?

It is highly customized, but was originally based on the basic [flaskr tutorial](http://flask.pocoo.org/docs/tutorial/introduction/), styled using Twitter's [Bootstrap](http://twitter.github.com/bootstrap/) CSS framework.

What have I added?
* Permalinks for each blog post
* A model to collect beer recipes, in addition to narrative blog posts
* A fully functional entry admin using [Flask-Peewee](https://github.com/coleifer/flask-peewee/)
* A secure auth system, with password hashing, using Flask-Peewee
* Database persistence using PostgreSQL
* Interaction with the database using the [Peewee ORM](https://peewee.readthedocs.org/en/latest/index.html) instead of straight SQL
* Easy hosting for the application on Heroku

The development of this application is ongoing, but you can see a live version deployed at http://carboy.tommeagher.com/

The current alpha version is 0.6.0.