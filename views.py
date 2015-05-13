from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import re
from datetime import date, datetime

from app import app, psql_db
from auth import auth
from models import User, Entry, Page
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
    perpage=10
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
    pagecount=calc_entries()
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
    return pagecount

@app.route('/entry-list/<pagenum>/')
def new_page(pagenum):
    if pagenum=='admin':
        return redirect(url_for(admin))
    else:
        pagenum=int(pagenum)
        return show_entries(page=pagenum)
    
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
