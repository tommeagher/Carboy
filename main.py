from app import app, psql_db
from auth import *
from admin import admin
from models import *
from views import *

def create_tables():
    psql_db.connect()
    psql_db.create_tables([Entry, User, Page, Recipe], safe=True)
    return

if __name__ == '__main__':

    create_tables()
    app.run()