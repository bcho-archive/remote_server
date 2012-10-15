#coding: utf-8

from flask import Blueprint, request

from server.base import db, logger
from server.models import User, Bot
from server.config import qqweibot_callback_uri

app = Blueprint('weibot', __name__)


@app.route('/qq/callback', methods=['GET'])
def qq_weibo_get_code():
    code = request.args['code']
    openid = request.args['openid']
    openkey = request.args['openkey']

    u = db.session.query(User).filter(User.openid == openid)
    if u.count():
        u = u.one()
    else:
        qqbot = db.session.query(Bot).filter(Bot.type == 1).one()
        bot = qqbot.build_bot()
        resp = bot.request_access_token(code)
        resp.openid = openid
        resp.openkey = openkey
        u = User()
        u.assign(resp)
        db.session.add(u)
        db.session.commit()
        logger.info('Created new user <%s %s>' % (u.name, u.openid))

    if not u.token:
        u.generate_token()

    return 'your arm server token: %s' % (u.token)


@app.route('/qq', methods=['GET'])
def qq_login():
    qqbot = db.session.query(Bot).filter(Bot.type == 1).one()
    bot = qqbot.build_bot()
    return '<a href="%s">login with your qq weibo account here.</a>' % (
            bot.get_authorize_url())


@app.route('/qqbot/callback', methods=['GET'])
def qqbot_callback():
    code = request.args['code']
    openid = request.args['openid']
    openkey = request.args['openkey']

    qqbot = db.session.query(Bot).filter(Bot.type == 1).one()
    bot = qqbot.build_bot(qqweibot_callback_uri)
    resp = bot.request_access_token(code)
    resp.openid = openid
    resp.openkey = openkey

    qqbot.assign(resp)
    db.session.commit()
    logger.info('Updated qq bot info <%s %s>' % (qqbot.name, qqbot.openid))

    return 'OK'


@app.route('/qqbot', methods=['GET'])
def qqbot_auhorize():
    qqbot = db.session.query(Bot).filter(Bot.type == 1).one()
    bot = qqbot.build_bot(qqweibot_callback_uri)
    return '<a href="%s">bot, login here.</a>' % (
            bot.get_authorize_url())
