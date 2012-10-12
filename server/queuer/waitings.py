#coding: utf-8

from datetime import datetime

from server.base import db
from server.models import Job
from server.translator import human2machine


def enqueue(action):
    action, action_t = human2machine(action)
    job = Job()
    job.action = action
    job.type = action_t
    job.status = 0
    job.added_time = datetime.utcnow()
    db.session.add(job)
    db.session.commit()
    return job


def get(user_id):
    jobs = db.session.query(Job).filter(
         Job.user_id == user_id).order_by(
         Job.added_time)
    if jobs.count():
        return jobs.all()[0]
    else:
        return None
