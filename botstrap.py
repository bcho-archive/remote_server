#coding: utf-8

from server.base import db
from server.models import Bot

qqbot = db.session.query(Bot).filter(Bot.type == 1).one().weibot
