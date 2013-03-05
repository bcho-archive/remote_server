#coding: utf-8

from flask import Flask

from db import db
from utils import register_blueprint
from config import blueprints


#: init app
app = Flask(__name__)
app.config.from_pyfile('config.py')


#: register blueprints
for blueprint in blueprints:
    register_blueprint(app, blueprint)


#: init db
db.init_app(app)
db.app = app
