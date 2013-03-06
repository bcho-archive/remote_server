#coding: utf-8

from flask import Blueprint, url_for, request

from server.base import db

import config
from models import OfflineUser

app = Blueprint('offline', __name__)


def register_user(user_id, weibo_token, is_bot=None):
    user = OfflineUser.query.filter_by(user_id=user_id).first()
    if not user:
        user = OfflineUser(user_id, weibo_token, is_bot)
        db.session.add(user)
    else:
        if user.weibo_token != weibo_token:
            user.weibo_token = weibo_token
            user.token = user.generate_token(weibo_token)
    db.session.commit()
    return user.token


@app.route('/')
def startpoint():
    return '''<a href="%s/setup?callback=127.0.0.1:5000%s">
setup your token here</a>''' % \
        (config.offline_uri, url_for('.callback'))


@app.route('/callback')
def callback():
    token = register_user(int(request.args['user_id']), request.args['token'])
    return 'your arm server token: %s' % (token)


@app.route('/bot')
def bot_startpoint():
    return '''<a href="%s/setup?callback=127.0.0.1:5000%s">
setup your token here</a>''' % \
        (config.offline_uri, url_for('.bot_callback'))


@app.route('/bot_callback')
def bot_callback():
    register_user(int(request.args['user_id']), request.args['token'], True)
    return 'ok'
