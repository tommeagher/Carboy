from flask_peewee.admin import Admin, ModelAdmin, AdminPanel
from flask import request, redirect
from auth import auth

from models import *
from app import app, psql_db

class EntryAdmin(ModelAdmin):
    columns = ('title', 'publishdate', 'private')
    def get_query(self):
    	return Entry.select().order_by(-Entry.publishdate)

class UserAdmin(ModelAdmin):
    columns = ('username', 'email',  'twitter', 'admin', 'active')

class RecipeAdmin(ModelAdmin):
    def get_query(self):
    	return Recipe.select().order_by(Recipe.slug)

class PageAdmin(ModelAdmin):
    def get_query(self):
    	return Page.select().order_by(-Page.publishdate)

admin = Admin(app, auth, branding = "Carboy admin")

auth.register_admin(admin)
admin.register(Entry, EntryAdmin)
admin.register(Page, PageAdmin)
admin.register(Recipe, RecipeAdmin)
admin.register(User, UserAdmin)

admin.setup()