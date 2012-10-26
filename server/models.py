#coding: utf-8

from sha import sha
from datetime import datetime
from random import random

from flask.ext.sqlalchemy import SQLAlchemy

from server.weibot.api import SinaClient, QClient

db = SQLAlchemy()
session = db.session


class DictModel(object):
    '''Provides keys() and items().
    The keys() is columns.
    The value will return serializated data'''

    #: not all things can be changed in assign
    assignable_keywords = []

    def assign(self, p):
        p = {} if not p else p
        for k, v in p.items():
            if k in self.assignable_keywords:
                setattr(self, k, v)

    def keys(self):
        return self.__table__.columns._data.keys()

    def items(self):
        return [(k, getattr(self, k)) for k in self.keys()]


class User(db.Model, DictModel):
    assignable_keywords = ['name', 'access_token', 'expires_in',
                           'refresh_token', 'weibo_id',
                           'openkey', 'openid']
    bot = None

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, default=1)  # 0: sina weibo, 1: qq weibo
    # for identifying the arm server
    # make it shorter: ok, we only generate a 5 character token,
    #                  which means, we can only support
    #                  36^5 = 60466176 users. I think it's
    #                  enough...
    token_length = 5
    token = db.Column(db.String(5), unique=True)

    # weibo user infomations
    name = db.Column(db.String(100))
    weibo_id = db.Column(db.String(150))  # qq weibo uses openid
    access_token = db.Column(db.String(200))
    expires_in = db.Column(db.String(200))
    refresh_token = db.Column(db.String(200))
    # use in qq weibo
    openkey = db.Column(db.String(200))
    openid = db.Column(db.String(200))

    # one to many
    jobs = db.relationship('Job', backref='user')

    def generate_token(self):
        def build_token(salt, l=self.token_length):
            return sha(self.name + self.access_token + salt).hexdigest()[0:l]

        salt = datetime.utcnow().strftime('%y%m%d%H%M%S') + str(random())
        token = build_token(salt)
        while session.query(User).filter(User.token == token).count():
            token = build_token(salt)
        self.token = token
        session.commit()
        return token

    def attach_bot(self):
        bot = session.query(Bot).filter(Bot.type == self.type)
        if bot.count():
            bot = bot.all()[0].build_bot()
        else:
            bot = None
        self.bot = bot

    def get_bot(self):
        if self.type == 0:
            self.bot.set_access_token(self.access_token, self.expires_in)
        elif self.type == 1:
            self.bot.set_access_token(self.access_token, self.openid,
                                      self.expires_in)
        return self.bot

    def refresh_weibo_token(self):
        # TODO auto refresh
        #      Refreshtoken is abolished in qq weibo
        if not self.bot:
            self.attach_bot()
        #: is qq weibo
        if self.type == 1:
            self.assign(self.bot.refresh_token(self.refresh_token))
            session.commit()
            return True
        else:
            return None


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(1000))
    # 0 waiting 1 doing 2 finished(not report yet) 3 reported
    status = db.Column(db.Integer, default=0)
    # 0 action 1 quering
    type = db.Column(db.Integer)
    report = db.Column(db.String(5000))
    added_time = db.Column(db.DateTime())
    tweet_id = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Bot(db.Model, DictModel):
    assignable_keywords = ['name', 'access_token', 'expires_in',
                           'refresh_token', 'weibo_id', 'openkey',
                           'openid', 'app_key', 'app_secret', 'redirect_uri']
    bot = None

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, default=1)  # 0: sina weibo, 1: qq weibo

    # weibo user infomations
    name = db.Column(db.String(100))
    weibo_id = db.Column(db.String(150))
    access_token = db.Column(db.String(200))
    expires_in = db.Column(db.String(200))
    refresh_token = db.Column(db.String(200))
    # use in qq weibo
    openkey = db.Column(db.String(200))
    openid = db.Column(db.String(200))

    # app infomations
    app_key = db.Column(db.String(100))
    app_secret = db.Column(db.String(100))
    redirect_uri = db.Column(db.String(1000))

    def build_bot(self, redirect_uri=None):
        client = QClient if self.type else SinaClient
        redirect_uri = redirect_uri or self.redirect_uri
        bot = client(self.app_key, self.app_secret, redirect_uri)
        return bot

    @property
    def weibot(self):
        if not getattr(self, 'bot'):
            client = QClient if self.type else SinaClient
            bot = client(self.app_key, self.app_secret, self.redirect_uri)
            if self.type == 0:
                bot.set_access_token(self.access_token, self.expires_in)
            elif self.type == 1:
                bot.set_access_token(self.access_token, self.openid,
                                     self.expires_in)
            setattr(self, 'bot', bot)
        return self.bot
