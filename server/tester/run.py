#coding: utf-8

'''
    run
    ~~~

    Run offline tester
'''

from time import sleep

from server.base import logger, db
from server.models import User
from server.queuer import reports, waitings, unknown
from .generator import tweets


# uhh, some duplicated code here...
def send():
    report = reports.get()
    if report:
        if report.name == 'query' and report.obj == 'all' or \
                report.name == 'capture':
            logger.info('post image')
        else:
            logger.info('sent report <%s>' % (report.report))
        reports.archive(report.id)
        logger.info('archived job <%d %s>' % (report.id, report.action))


def handle_commands(commands):
    def _is_user(name):
        return db.session.query(User).filter(User.name == name).count() > 0

    for command in commands:
        if not waitings.in_queue(command.id) and _is_user(command.name) and\
                not unknown.in_queue(command.id):
            new_job = waitings.enqueue(command.text, command.id, command.name)
            if new_job:
                logger.info('found new job <%d %s>' % (
                                    new_job.id, new_job.action))
            else:
                unknown.enqueue(command.id, command.text)


# TODO clean the test job
def run(sleep_time=None):
    sleep_time = sleep_time or 200
    t = tweets()
    while True:
        if not t:
            t = tweets()
        handle_commands([t.pop()])
        send()
        sleep(sleep_time)
