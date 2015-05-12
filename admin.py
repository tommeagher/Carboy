import flask_admin as admin
from flask_admin import form
from flask_admin.form import rules
from models import *
from app import app
from wtforms import PasswordField
from flask_admin.contrib.peewee import ModelView

class UserAdmin(ModelView):
    form_columns = ('username', 'password', 'email', 'twitter', 'join_date', 'active', 'admin')

    column_searchable_list={'username'}
    column_exclude_list = ['password']
    

class EntryAdmin(ModelView):
    # Visible columns in the list view
    column_exclude_list = ['text']

    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ('title', ('user', User.email), 'publishdate')

    # Full text search
    column_searchable_list = ('title', User.username)

    # Column filters
    column_filters = ('title',
                      'publishdate',
                      User.username)

    form_ajax_refs = {
        'user': {
            'fields': (User.username, 'email')
        }
    }

    form_create_rules = [
        # Define field set with header text and four fields
        rules.FieldSet(('title', 'subhed', 'text', 'publishdate', 'stage', 'private', 'user'), 'Entry')
        # ... and it is just shortcut for:
    ]
    form_edit_rules=form_create_rules

class PageAdmin(ModelView):
    # Visible columns in the list view
    column_exclude_list = ['text']

    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ('title', ('user', User.email), 'publishdate')

    # Full text search
    column_searchable_list = ('title', User.username)

    # Column filters
    column_filters = ('title',
                      'publishdate',
                      User.username)

    form_ajax_refs = {
        'author': {
            'fields': (User.username, 'email')
        }
    }

    form_create_rules = [
        # Define field set with header text and four fields
        rules.FieldSet(('title', 'text', 'publishdate', 'author'), 'Entry')
        # ... and it is just shortcut for:
    ]
    form_edit_rules=form_create_rules

admin = admin.Admin(app, name='Carboy admin')

admin.add_view(UserAdmin(User))
admin.add_view(EntryAdmin(Entry))
admin.add_view(PageAdmin(Page))