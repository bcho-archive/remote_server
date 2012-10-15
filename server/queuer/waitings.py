#coding: utf-8

from datetime import datetime

from server.base import db, logger
from server.models import Job, User
from server.translator import human2machine


def enqueue(action, tweet_id, username):
    action, action_t = human2machine(action)
    user = db.session.query(User).filter(User.name == username).one()
    job = Job()
    job.action = action
    job.tweet_id = tweet_id
    job.type = action_t
    job.status = 0
    job.added_time = datetime.utcnow()
    db.session.add(job)
    job.user = user
    logger.debug(user.name)
    db.session.commit()
    return job


def in_queue(tweet_id):
    return db.session.query(Job).filter(Job.tweet_id == tweet_id).count() > 0


def get(user_id):
    jobs = db.session.query(Job).filter(
         Job.user_id == user_id, Job.status == 0).order_by(
         Job.added_time)
    if jobs.count():
        return jobs.all()[0]
    else:
        return None
