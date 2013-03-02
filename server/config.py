#coding: utf-8

import os
import logging


parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(parent, 'data')

#: XXX DEV database path
database = os.path.join(data_path, 'remote_dev.sqlite')
database_url = 'sqlite:///%s' % database
SQLALCHEMY_DATABASE_URI = database_url

#: basic config
SITE_TITLE = 'remote server'
project_codename = 'server'  # for initing blueprint
datetime_format = '%Y-%m-%d %H:%M:%S'
image_path = os.path.join(data_path, 'imgs')
unknown_command_path = os.path.join(parent, 'data', 'unkown.txt')
unknown_command_log = 'unknown_command.log'

logger_name = project_codename
log_path = '%s.log' % project_codename
log_format = '%(levelname)s - %(message)s'
#: XXX DEV
log_level = logging.DEBUG

#: tester
tester = {
        'id': 'bcxxxxxx',
        'raw': os.path.join(data_path, 'raw.txt')
}

# weibot key & secret
# 0: sina weibo 1: qq weibo
weibot = {
        0: {
            'app_key': '2866534204',
            'app_secret': '7a6ca5d4a02171678ff0e1605dbc1a8c',
            'redirect_uri': 'http://itunesplaying.jactry.com/callback.php'
        },
        1: {
            'app_key': '801251861',
            'app_secret': '21565ddc17a12bae12260eed8188bcee',
            'redirect_uri': 'http://127.0.0.1:5000/weibot/qq/callback'
        }
}
qqweibot_callback_uri = 'http://127.0.0.1:5000/weibot/qqbot/callback'

#: XXX DEV
DEBUG = True
