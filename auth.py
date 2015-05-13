from flask_peewee.auth import Auth

from app import app, psql_db
from models import User


auth=Auth(app, psql_db, user_model=User)