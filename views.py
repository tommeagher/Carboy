from urlparse import urljoin
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import re
from datetime import date, datetime

from werkzeug.contrib.atom import AtomFeed
from app import app, psql_db
from auth import auth
from models import User, Entry, Page, Recipe
from admin import admin
from math import ceil


#create db connections for functions
@app.before_request
def _db_connect():
    psql_db.connect()

@app.teardown_request
def _db_close(exc):
    if not psql_db.is_closed():
        psql_db.close()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
    
@app.route('/')
def show_entries(page=1):
    pagecount, perpage = calc_entries()
    entries = Entry.select().order_by(-Entry.publishdate).paginate(int(page), perpage)

    for entry in entries:
        entry.year = entry.publishdate.year

        if len(str(entry.publishdate.month))==1:
            entry.month="0"+str(entry.publishdate.month)
        else:
            entry.month=entry.publishdate.month
        if len(str(entry.publishdate.day))==1:
            entry.day="0"+str(entry.publishdate.day)
        else:
            entry.day=entry.publishdate.day
        entry.twitter = User.get(User.id==entry.user).twitter
    
    page=int(page)
    if page>1:
        entries.newer=page-1
    else:
        entries.newer=None
    if pagecount>page:
        entries.older=page+1
    else:
        entries.older=None
    return render_template('show_entries.html', entries=entries)

def calc_entries():
    paginate=10
    entrycount = Entry.select().count()
    if entrycount>paginate:
        pagecount = ceil(entrycount/float(paginate))
    else:
        pagecount=1
    return pagecount, paginate

@app.route('/entry-list/<pagenum>/')
def new_page(pagenum):
    if pagenum=='admin':
        return redirect(url_for(admin))
    else:
        pagenum=int(pagenum)
        return show_entries(page=pagenum)

@app.route('/entries/<year>/<month>/<slug>.html')
def show_entry(slug, year, month):
    entry = Entry.select().where(Entry.publishdate.year==year).where(Entry.publishdate.month==month).where(Entry.slug==slug).get()

    entry.year = entry.publishdate.year
    if len(str(entry.publishdate.month))==1:
        entry.month="0"+str(entry.publishdate.month)
    else:
        entry.month=entry.publishdate.month
    if len(str(entry.publishdate.day))==1:
        entry.day="0"+str(entry.publishdate.day)
    else:
        entry.day=entry.publishdate.day
    entry.twitter = User.get(User.id==entry.user).twitter
    if entry is None:
        abort(404)
    else:
        return render_template('entry.html', entry=entry)

@app.route('/recipes/')
def show_recipes(page=1):
    pagecount, perpage=calc_recipes()
    recipes = Recipe.select().order_by(Recipe.title).paginate(int(page), perpage)

    page=int(page)
    if page>1:
        recipes.newer=page-1
    else:
        recipes.newer=None
    if pagecount>page:
        recipes.older=page+1
    else:
        recipes.older=None
    return render_template('show_recipes.html', recipes=recipes)

def calc_recipes():
    paginate=25
    recipecount = Recipe.select().count()
    if recipecount>paginate:
        pagecount = ceil(recipecount/float(paginate))
    else:
        pagecount=1
    return pagecount, paginate

@app.route('/recipe-list/<pagenum>/')
def new_recipe_page(pagenum):
    if pagenum=='admin':
        return redirect(url_for(admin))
    else:
        pagenum=int(pagenum)
        return show_recipes(page=pagenum)
    
@app.route('/recipes/<slug>.html')
def show_recipe(slug):
    recipe = Recipe.select().where(Recipe.slug==slug).get()

    recipe.year = recipe.added_date.year
    if len(str(recipe.added_date.month))==1:
        recipe.month="0"+str(recipe.added_date.month)
    else:
        recipe.month=recipe.added_date.month
    if len(str(recipe.added_date.day))==1:
        recipe.day="0"+str(recipe.added_date.day)
    else:
        recipe.day=recipe.added_date.day

    if recipe is None:
        abort(404)
    else:
        return render_template('recipe.html', recipe=recipe)

@app.route('/<pagename>.html')
def show_page(pagename):
    try:
        page = Page.get(Page.slug==str(pagename))
        if page is None:
            abort(404)
        else:
            return render_template('page.html', page=page)
    except:
        abort(404)

@app.route('/recent.atom')
def recent_feed():
    feed=AtomFeed('Recent Posts',
        feed_url=request.url, url=request.url_root)
    posts = Entry.select().order_by(-Entry.publishdate).limit(15)
    for post in posts:
        post.year = post.publishdate.year
        if len(str(post.publishdate.month))==1:
            post.month="0"+str(post.publishdate.month)
        else:
            post.month=post.publishdate.month

        feed.add(post.title, unicode(post.text), content_type='html',
            author = post.user.user_first+' '+post.user.user_last,
            url = 'http://carboy.tommeagher.com/entries/{0}/{1}/{2}'.format(post.year, post.month, post.slug),
            published = datetime.combine(post.publishdate, datetime.min.time()), updated=datetime.combine(post.publishdate, datetime.min.time()))

    return feed.get_response()

