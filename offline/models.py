#coding: utf-8

import logging
from sha import sha
from datetime import datetime
from time import time

import config
from db import db
from logger import get_console_logging_handler as console_logger

logger = logging.getLogger(__name__)
logger.setLevel(config.log_level)
logger.addHandler(console_logger(config.log_format, config.log_level))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(40))
    api_token = db.Column(db.String(40), unique=True)
    login_token = db.Column(db.String(40), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = self.encrypt(password + config.secret_key)

    def encrypt(self, raw=None):
        raw = raw or str(time())
        return sha(raw).hexdigest()

    @staticmethod
    def is_name_unique(username):
        return User.query.filter_by(username=username).count() < 1

    def tweets(self, limit=None):
        if not self.id:
            logger.debug('id not set yet')
            return
        return Tweet.query.filter_by(author_id=self.id).limit(limit).all()

    @property
    def mentions(self):
        mentions = Mention.query.filter_by(user_id=self.id).all()
        return [i.tweet_id for i in mentions]

    def login(self, password):
        if self.encrypt(password + config.secret_key) == self.password:
            self.login_token = self.encrypt(self.username + str(time()))
            return self.login_token
        return None


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    #: share one folder, use image filename
    image = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.now)
    retweet_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)

    def __init__(self, content, author_id, image=None, retweet_id=None):
        self.content = content
        self.author_id = author_id
        if image:
            self.image = image
        if retweet_id:
            self.retweet_id = retweet_id

    @property
    def author(self):
        return User.query.filter_by(id=self.author_id).first()

    @property
    def origin(self):
        return Tweet.query.filter_by(id=self.retweet_id).first()

    def retweets(self, limit=None):
        if not self.id:
            logger.debug('id not set yet')
            return
        return Tweet.query.filter_by(retweet_id=self.id).limit(limit).all()


class Mention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    tweet_id = db.Column(db.Integer)

    def __init__(self, user_id, tweet_id):
        self.user_id = user_id
        self.tweet_id = tweet_id

    @staticmethod
    def validate(user_id, tweet_id):
        _v = lambda m, i: m.query.filter_by(id=i).count == 0
        return not any(map(_v, [User, Tweet], [user_id, [tweet_id]]))

    @property
    def user(self):
        return User.query.filter_by(id=self.user_id).first()

    @property
    def tweet(self):
        return Tweet.query.filter_by(id=self.tweet_id).first()
