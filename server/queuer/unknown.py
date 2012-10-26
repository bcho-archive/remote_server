#coding: utf-8

'''
    unknown
    ~~~~~~~
    Holding the unknown orders from the user.
'''

from server.base import db
from server.models import Job


def in_queue(id):
    return id in db.session.query(Job).filter(Job.status == -1).all()


def enqueue(id):
    if not in_queue(id):
        j = Job()
        j.status, j.tweet_id = -1, id
        db.session.add(j)
        db.session.commit()
        return j
    else:
        return db.session.query(Job).filter(
                Job.status == -1, Job.tweet_id == id).one()
