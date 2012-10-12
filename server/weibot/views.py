#coding: utf-8

from flask import Blueprint, request

from server.base import db
from server.models import User, Bot

app = Blueprint('weibot', __name__)
qqbot = db.session.query(Bot).filter(Bot.type == 1).one()


@app.route('/qq/callback', methods=['GET'])
def get_code():
    code = request.args['code']
    openid = request.args['openid']
    openkey = request.args['openkey']

    u = db.session.query(User).filter(User.openid == openid)
    if u.count():
        u = u.one()
    else:
        resp = qqbot.request_access_token(code)
        resp.openid = openid
        resp.openkey = openkey
        u = User()
        u.assign(resp)
        db.session.add(u)
        db.commit()

    if not u.token:
        u.generate_token()

    return 'your arm server token: %s' % (u.token)


@app.route('/qq', method=['GET'])
def qq_login():
    return '<a href="%s">login with your qq weibo acount here.</a>' % (
            qqbot.get_authorize_url())
