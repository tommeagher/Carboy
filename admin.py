from flask_peewee.admin import Admin, ModelAdmin, AdminPanel
from flask import request, redirect
from auth import auth

from models import *
from app import app, psql_db

class EntryAdmin(ModelAdmin):
    columns = ('title', 'publishdate', 'private')

class UserAdmin(ModelAdmin):
    columns = ('username', 'email',  'twitter', 'admin', 'active')


admin = Admin(app, auth, branding = "Carboy admin")

auth.register_admin(admin)
admin.register(Entry, EntryAdmin)
admin.register(Page)
admin.register(User, UserAdmin)

admin.setup()