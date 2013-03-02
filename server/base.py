#coding: utf-8

import logging

from flask import Flask

import config
from models import db
from logger import get_file_logging_handler as file_logger 
from logger import get_console_logging_handler as console_logger

#: init logger
logger = logging.getLogger(__name__)
logger.setLevel(config.log_level)
formatter = logging.Formatter(config.log_format)
for i in [console_logger, file_logger]:
    logger.addHandler(i(formatter))

#: init app
app = Flask(__name__)
app.config.from_pyfile('config.py')

#: init database
db.init_app(app)
db.app = app
