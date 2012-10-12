#coding: utf-8

import os


#: XXX DEV database path
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database = os.path.join(parent, 'data', 'remote_dev.sqlite')
database_url = 'sqlite:///%s' % database
SQLALCHEMY_DATABASE_URI = database_url

#: basic config
SITE_TITLE = 'remote server'
project_codename = 'server'  # for initing blueprint
datetime_format = '%Y-%m-%d %H:%M:%S'

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
            'redirect_uri': 'http://127.0.0.1:5000/weibot/callback'
        }
}

#: XXX DEV
DEBUG = True
