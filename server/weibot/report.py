#coding: utf-8

from server.base import db
from server.models import Bot
from server.queuer import reports

qqbot = db.session.query(Bot).filter(Bot.type == 1).one().weibot


def send():
    report = reports.get()
    if report:
        qqbot.post.update(content=report.report)
        reports.archive(report.id)
        return 1
    else:
        return 0
