import datetime
import re
from peewee import *

from app import psql_db, BaseModel

def slugify(string):
    # Generate a URL-friendly representation of the entry's title.
    string = re.sub(r"[^\w]+", " ", string)
    string = "-".join(string.lower().strip().split())
    return string

class User(BaseModel):
    username = CharField()
    user_last=CharField()
    user_first=CharField()
    password = CharField()
    email = CharField()
    twitter = CharField(null=True)
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username

class Entry(BaseModel):
    title = CharField()
    subhed = TextField(null=True)
    text = TextField(null=True)
    publishdate = DateField(default=datetime.datetime.now().date())
    stage = CharField(choices=(('Thirsty','Thirsty'),('Brewing','Brewing'),('Primary','Primary'),('Secondary','Secondary'),('Bottling','Bottling'),('Enjoying','Enjoying')))
    private = BooleanField(default=False)
    slug = CharField(null=True)
    user = ForeignKeyField(User, related_name='Entries')

    def save(self, *args, **kwargs):
        # Add a URL-friendly representation of the entry's title.
        self.slug = slugify(self.title)
        ret = super(Entry, self).save(*args, **kwargs)
        return ret

    def __unicode__(self):
        return self.title

class Page(BaseModel):
    title = CharField()
    text = TextField(null=True)
    publishdate = DateField(default=datetime.datetime.now().date())
    slug = CharField(null=True)
    author= ForeignKeyField(User, related_name='Pages')

    def save(self, *args, **kwargs):
        # Add a URL-friendly representation of the entry's title.
        self.slug = slugify(self.title)
        ret = super(Page, self).save(*args, **kwargs)
        return ret

    def __unicode__(self):
        return self.title