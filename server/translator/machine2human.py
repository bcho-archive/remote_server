#coding: utf-8

from .dictionary import en_d as d
from .dictionary import s


def machine2human(report):
    action, obj = d.get(report['action'])[0], d.get(report['obj'])[0]
    status, action_type = report['status'], int(report['type'])

    #: is an action
    if action_type == 0:
        return s[status](action=action, obj=obj)

    #: is a query
    if action_type == 1 and report['obj'] != 'all':
        return s['query'](action=action, obj=obj, **status)

    #: is a query all
    if action_type == 1 and report['obj'] == 'all':
        return s['query_all'](action=action, obj=obj, **status)
