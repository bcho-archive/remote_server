#coding: utf-8

# XXX ATTENTION everythings in current is readonly!
#               don't try to change them, because you
#               can't access to the origin session.

from server.base import db
from server.models import Bot

bot = db.session.query(Bot).filter(Bot.type == 1).one().weibot
