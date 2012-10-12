#coding: utf-8

from flask import Flask

from models import db

#: init app
app = Flask(__name__)
app.config.from_pyfile('config.py')

#: init database
db.init_app(app)
db.app = app
