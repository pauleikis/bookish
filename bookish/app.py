from flask import Flask
from flask_bootstrap import Bootstrap

from peewee import SqliteDatabase


app = Flask(__name__)
app.config.from_object('bookish.config.default')

Bootstrap(app)

db = SqliteDatabase(app.config['DATABASE'])


import bookish.views