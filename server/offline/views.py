#coding: utf-8

from flask import Blueprint, url_for, request

from server.base import db
from server.models import User, Bot

import config

app = Blueprint('offline', __name__)


def register_user(user_name, user_id, weibo_token, is_bot=None):
    if is_bot:
        user = Bot()
        user.name, user.weibo_id, user.access_token = (user_name, user_id, 
                weibo_token)
        user.type = 2
        db.session.add(user)
        db.session.commit()
    else:
        user = User.query.filter_by(weibo_id=user_id).first()
        if user:
            user.access_token, user.name = weibo_token, user_name
            db.session.commit()
        else:
            user = User()
            user.name, user.weibo_id, user.access_token = (user_name, user_id, 
                    weibo_token)
            db.session.add(user)
            db.session.commit()
        return user.generate_token()


@app.route('/')
def startpoint():
    return '''<a href="%s/setup?callback=127.0.0.1:5000%s">
setup your token here</a>''' % \
        (config.offline_uri, url_for('.callback'))


@app.route('/callback')
def callback():
    token = register_user(request.args['user_name'],
            request.args['user_id'], request.args['token'])
    return 'your arm server token: %s' % (token)


@app.route('/bot')
def bot_startpoint():
    return '''<a href="%s/setup?callback=127.0.0.1:5000%s">
setup your token here</a>''' % \
        (config.offline_uri, url_for('.bot_callback'))


@app.route('/bot_callback')
def bot_callback():
    register_user(request.args['user_name'],
            request.args['user_id'], request.args['token'], True)
    return 'ok'
