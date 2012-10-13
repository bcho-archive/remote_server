#coding: utf-8

from server.base import db
from server.models import User
from server.queuer import reports, waitings

from .current import bot


def send():
    report = reports.get()
    if report:
        resp = bot.post.t__add(content=report.report)
        reports.archive(report.id)
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
            waitings.enqueue(mention.text, mention.id)
