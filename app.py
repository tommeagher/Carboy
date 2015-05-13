from flask import Flask
from peewee import *
from playhouse.db_url import connect
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

psql_db = connect(os.environ.get('DATABASE_URL') or os.environ.get('LOCAL_DEV_DB_URL'))

class BaseModel(Model):
    class Meta:
        database = psql_db

app.debug=True
