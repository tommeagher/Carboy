import datetime
import re
from peewee import *
from flask_peewee.auth import BaseUser

from app import psql_db, BaseModel

def slugify(string):
    # Generate a URL-friendly representation of the entry's title.
    string = re.sub(r"[^\w]+", " ", string)
    string = "-".join(string.lower().strip().split())
    return string

class User(BaseModel, BaseUser):
    username = CharField()
    user_first=CharField(verbose_name="First name", null=True)
    user_last=CharField(verbose_name="Last name", null=True)
    password = CharField()
    email = CharField()
    twitter = CharField(null=True)
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def save(self, *args, **kwargs):
        #if the password is already hashed, then it hasn't changed and doesn't need to be re-hashed.
        if '$' in self.password:
            pass
        else:
            self.set_password(self.password)

        if self.twitter:
            if self.twitter[0]=='@':
                self.twitter = self.twitter[1:]
            else:
                self.twitter = self.twitter
        else:
            pass

        ret = super(User, self).save(*args, **kwargs)
        return ret

    def __unicode__(self):
        return self.username

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

class Recipe(BaseModel):
    title = CharField(verbose_name="Beer name")
    style = CharField(null=True)
    brew_type = CharField(choices=(('All-Grain','All-Grain'),('Partial','Partial'),('Extract','Extract')), default='All-Grain')
    recipe_URL = CharField(null=True)
    batch_size = CharField(null=True)
    abv = CharField(null=True)
    ibu = CharField(null=True)
    grains = TextField(null=True)
    hops = TextField(null=True)
    adjuncts = TextField(null=True)
    yeasts = TextField(null=True)
    source = CharField(null=True)
    source_URL = CharField(null=True)
    other_stats = TextField(null=True)
    mash = TextField(null=True)
    description = TextField(null=True)
    fermentation = TextField(null=True)
    added_date = DateField(default=datetime.datetime.now().date())
    slug = CharField(null=True)

    def save(self, *args, **kwargs):
        # Add a URL-friendly representation of the entry's title.
        self.slug = slugify(self.title)
        ret = super(Recipe, self).save(*args, **kwargs)
        return ret

    def __unicode__(self):
        return self.title

class Entry(BaseModel):
    title = CharField()
    subhed = TextField(null=True)
    text = TextField(null=True)
    publishdate = DateField(default=datetime.datetime.now().date())
    stage = CharField(choices=(('Thirsty','Thirsty'),('Brewing','Brewing'),('Primary','Primary'),('Secondary','Secondary'),('Bottling','Bottling'),('Enjoying','Enjoying')))
    private = BooleanField(default=False)
    slug = CharField(null=True)
    user = ForeignKeyField(User, related_name='Entries')
    recipe = ForeignKeyField(Recipe, related_name='Batch', null=True)

    def save(self, *args, **kwargs):
        # Add a URL-friendly representation of the entry's title.
        self.slug = slugify(self.title)
        ret = super(Entry, self).save(*args, **kwargs)
        return ret

    def __unicode__(self):
        return self.title