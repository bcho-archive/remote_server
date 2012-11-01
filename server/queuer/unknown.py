#coding: utf-8

'''
    unknown
    ~~~~~~~
    Holding the unknown orders from the user.
'''

from server.base import db
from server.models import Job
from server.config import unknown_command_path


def in_queue(id):
    return id in db.session.query(Job).filter(Job.status == -1).all()


def enqueue(id, text):
    if not in_queue(id):
        j = Job()
        j.status, j.tweet_id = -1, id
        db.session.add(j)
        db.session.commit()

        f = open(unknown_command_path, 'a')
        f.write('%s\n' % text.encode('utf-8'))
        f.close()

        return j
    else:
        return db.session.query(Job).filter(
                Job.status == -1, Job.tweet_id == id).one()
