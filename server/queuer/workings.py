#coding: utf-8

from server.base import db
from server.models import Job


_get = lambda x: db.session.query(Job).filter(x)


def enqueue(job_id):
    job = _get(Job.id == job_id)
    if job.count():
        job = job.one()
        job.status = 1
        db.session.commit()
        return job
    else:
        return None


def get(job_id):
    job = _get(Job.id == job_id and Job.status == 1)
    if job.count():
        job = job.one()
        return job
    else:
        return None
