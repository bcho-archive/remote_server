#coding: utf-8

import logging

from flask import Flask

from models import db
from config import log_path, log_format, log_level

#: init logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler(log_path)
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

#: init app
app = Flask(__name__)
app.config.from_pyfile('config.py')

#: init database
db.init_app(app)
db.app = app
