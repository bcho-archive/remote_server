#coding: utf-8

from server.base import db
from server.config import weibot
from server.models import Bot

print '=> creating tables'
db.create_all()

print '=> creating bots'
for i in weibot.keys():
    b = Bot()
    b.type = i
    b.assign(weibot[i])
    db.session.add(b)
    db.session.commit()
