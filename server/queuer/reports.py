#coding: utf-8

from server.base import db
from server.models import Job
from server.translator import machine2human


def enqueue(job_id, report):
    report = machine2human(report)
    job = db.session.query(Job).filter(Job.id == job_id)
    if job.count():
        job = job.one()
        job.report = report
        job.status = 2
        db.session.commit()
        return job
    else:
        return None


def get():
    job = db.session.query(Job).filter(Job.status == 2)
    if job.count():
        job = job.one()
        return job
    else:
        return None


def archive(job_id):
    job = db.session.query(Job).filter(Job.id == job_id, Job.status == 2)
    if job.count():
        job = job.one()
        job.status = 3
        db.session.commit()
        return job
    else:
        return None
