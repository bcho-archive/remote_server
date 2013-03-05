#coding: utf-8

from sha import sha
from datetime import datetime
from time import time

import config
from db import db
from logger import get_console_logging_handler as console_logger


logger = console_logger(config.log_format, config.log_level)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(40))
    api_token = db.Column(db.String(40), unique=True)
    login_token = db.Column(db.String(40), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = self.encrypt(password + config.secret_key)

    def encrypt(self, raw):
        return sha(raw).hexdigest()

    @staticmethod
    def is_name_unique(username):
        return User.query.filter_by(username=username).count() < 1

    def tweets(self, limit=None):
        if not self.id:
            logger.debug('id not set yet')
            return
        return Tweet.query.filter_by(author_id=self.id).limit(limit).all()

    def login(self, password):
        if self.encrypt(password + config.secret_key) == self.password:
            self.login_token = self.encrypt(self.username + str(time()))
            return self.login_token
        return None


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    image = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    retweet_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)

    def __init__(self, content, author_id, image=None, retweet_id=None):
        self.content = content
        self.author_id = author_id
        if image:
            self.image = image
        if retweet_id:
            self.retweet_id = retweet_id

    def author(self):
        return User.query.filter_by(id=self.author_id).first()

    def retweets(self, limit=None):
        if not self.id:
            logger.debug('id not set yet')
            return
        return Tweet.query.filter_by(retweet_id=self.id).limit(limit).all()
