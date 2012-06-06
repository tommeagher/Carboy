#all the imports
import sqlite3
#for a heavier-duty app, we could use sqlalchemy
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
import local_settings

#Link to config settings
#CARBOY_SETTINGS = 'local_settings.py'

#create our application
app = Flask(__name__)
app.config.from_object('local_settings')

#connect to db
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
        
#initialize the db
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())  
        db.commit()
        
#create db connections for functions
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()
    
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text, publish, stage from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], publish=row[2], stage=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text, publish, stage) values (?, ?, ?, ?)', [request.form['title'], request.form['text'], request.form['publish'], request.form['stage']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    
#fire up development server as a standalone application
if __name__ == '__main__':
    app.run()