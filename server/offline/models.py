#coding: utf-8

from datetime import datetime

from server.base import db


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    post_time = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.String(50), nullable=False)

    parent_id = db.Column(db.Integer)

    def __init__(self, content, user, pid=None):
        self.content, self.user, self.parent_id = content, user, pid

    @staticmethod
    def parent(self):
        if self.parent_id:
            return db.query.filter_by(id=self.parent_id).first()
        return None
