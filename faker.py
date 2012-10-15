#coding: utf-8

'''
    faker
    ~~~~~

    Acts like a human being, a server, a bot.
'''

import requests
import json

from server.base import db, logger
from server.models import User, Bot

bot = db.session.query(Bot).filter(Bot.type == 1).one()
qqbot = bot.weibot
user = db.session.query(User).filter(User.type == 1).all()[0]
user.attach_bot()
userbot = user.get_bot()

json_header = {'Content-Type': 'application/json'}
token = {'token': user.token}


def post_order(order):
    order = '@%s %s' % (bot.name, order)
    userbot.post.t__add(content=order)
    logger.info('new order <%s> post' % order)


def fetch_job():
    url = 'http://localhost:5000/arm/job'
    payload = json.dumps(token)
    resp = requests.get(url, data=payload, headers=json_header)
    logger.info('got response <%d>' % resp.status_code)
    if resp.status_code == 200:
        logger.info('new job <%d %s> fetched' % (
                            resp.json['id'], resp.json['action']))
    return resp.json


def report_job(job_id, report):
    url = 'http://localhost:5000/arm/job/%d' % job_id
    payload = token
    token['report'] = report
    payload = json.dumps(payload)
    resp = requests.put(url, data=payload, headers=json_header)
    logger.info('got response <%d>' % resp.status_code)
    return resp
