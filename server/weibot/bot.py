#coding: utf-8

from server.base import db, logger
from server.models import User
from server.queuer import reports, waitings

from .current import bot


def send():
    report = reports.get()
    if report:
        resp = bot.post.t__re_add(content=report.report, reid=report.tweet_id)
        reports.archive(report.id)
        logger.info('archived job <%d %s>' % (report.id, report.action))

        return resp
    else:
        return None


def fetch():
    def _is_user(name):
        return db.session.query(User).filter(User.name == name).count() > 0

    timeline = bot.get.statuses__mentions_timeline()
    mentions = timeline.data.info
    for mention in mentions:
        if not waitings.in_queue(mention.id) and _is_user(mention.name):
            new_job = waitings.enqueue(mention.text, mention.id, mention.name)
            logger.info('found new job <%d %s>' % (new_job.id, new_job.action))
