#coding: utf-8

from time import time
from sha import sha

from server.base import db


class OfflineUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    weibo_token = db.Column(db.String(40), unique=True)
    is_bot = db.Column(db.Integer, default=0)
    token = db.Column(db.String(5), unique=True)

    def __init__(self, user_id, weibo_token, is_bot=None):
        self.user_id, self.weibo_token = user_id, weibo_token
        self.token = self.generate_token(weibo_token)
        if is_bot:
            self.is_bot = 1


    def generate_token(self, salt):
        raw = '%s%s' % (time(), salt)
        while True:
            token = sha(raw).hexdigest()[0:5]
            if OfflineUser.query.filter_by(token=token).count() == 0:
                return token
