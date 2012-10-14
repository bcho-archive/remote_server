#coding: utf-8

from flask import Blueprint, request, abort, jsonify, Response

from server.base import db, logger
from server.models import User

from server.queuer import reports, waitings, workings

app = Blueprint('arm', __name__)


def auth():
    if request.json and request.json['token']:
        user = db.session.query(User).filter(
                User.token == request.json['token'])
        if user.count():
            return user.one()
        else:
            return None
    else:
        return None


@app.route('/job', methods=['GET'])
def request_job():
    user = auth()
    if not user:
        abort(403)
    job = waitings.get(user.id)
    if job:
        #: enqueue job to workings, and set the status to working
        workings.enqueue(job.id)
        logger.info('arm <%s %s> got new job <%d %s>' % (
                    user.name, user.token, job.id, job.action))
        return jsonify(action=job.action, id=job.id)
    else:
        abort(404)


@app.route('/job/<int:job_id>', methods=['PUT'])
def report_job(job_id):
    user = auth()
    if not user:
        abort(403)
    report = request.json['report']
    job = workings.get(job_id)
    if job:
        #: enqueue job to reports, and set the status to finished
        reports.enqueue(job_id, report=report)
        logger.info('got report <%d %s> from arm <%s %s>' % (
                    job_id, report, user.name, user.token))
        return Response(status=204)
    else:
        abort(404)
