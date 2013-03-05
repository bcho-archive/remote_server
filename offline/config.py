#coding: utf-8

import os
import logging


parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(parent, 'data')

#: basic config
project_codename = 'snsh_offline'
datetime_format = '%Y-%m-%d %H:%M:%S'
image_path = os.path.join(data_path, 'imgs')

#: database
database = os.path.join(data_path, 'offline.sqlite')
database_url = 'sqlite:///%s' % database
SQLALCHEMY_DATABASE_URI = database_url

#: logging
logger_name = project_codename
log_path = '%s.log' % project_codename
log_format = '%(levelname)s - %(message)s'
log_level = logging.DEBUG

#: enabled blueprints
blueprints = []

#: security
secret_key = 'snsh'
SECRET_KEY = 'snsh'

#: debug
DEBUG = True
