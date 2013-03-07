#coding: utf-8

import requests

from server.base import logger
from server.queuer import reports, waitings, unknown
from server.translator.dictionary import s

from server.models import Bot as BotModel
from server.models import User
import config


class Bot(object):
    api_uri = config.offline_uri

    def __init__(self):
        self.bot = BotModel.query.filter_by(type=2).first()

    def repost(self, somethings, repost_id):
        data = {
                'content': somethings,
                'retweet_id': repost_id
        }
        params = {
                'token': self.bot.access_token        
        }
        return requests.post('%s/retweet' % self.api_uri,
                data=data, params=params)

    def upload_image(self, somethings, image_name, someone):
        data = {
                'content': '@%s: %s' % (someone, somethings),
                'image': image_name
        }
        params = {
                'token': self.bot.access_token        
        }
        return requests.post('%s/tweet', data=data, params=params)

    def send(self):
        report = reports.get()
        if report:
            if report.type == 1 and report.obj == 'all':
                resp = self.upload_image(report.report. str(report.id),
                                         report.user.name)
            else:
                resp = self.repost(report.report, report.id)
            reports.archive(report.id)
            logger.info('archived job <%d %s>' % (report.id, report.action))
            return resp
        else:
            return None

    def handle_commands(self, commands):
        def _is_user(name):
            return User.query.filter_by(name=name).count() > 0

        for command in commands:
            if not waitings.in_queue(command['id']) and \
                    _is_user(command['name']) and \
                    not unknown.in_queue(command['id']):
                new_job = waitings.enqueue(command['content'],
                        command['id'], command['name'])
                if new_job:
                    logger.info('found new job <%d %s>' % (
                            new_job.id, new_job.action))
                else:
                    unknown.enqueue(command['id'], command['content'])
                    self.repost(s['unknowncommand'](), command['id'])

    def fetch(self):
        params = {
                'token': self.bot.access_token
        }
        resp = requests.get('%s/mention' % self.api_uri, params=params)
        mentions = resp.json['mentions']
        self.handle_commands(mentions)

bot = Bot()
