#coding: utf-8

from .dictionary import en_d as d
from .dictionary import s, action_type_d


def machine2human(report):
    action, obj = d.get(report['action'])[0], d.get(report['obj'])[0]
    status, action_type = report['status'], action_type_d[action]
    if action is 'query' and report['obj'] is 'all':
        action_type = action_type_d['query_all']

    if action_type.name in ['turnon', 'turnoff']:
        return s[status](action=action, obj=obj)
    elif action_type.name is 'capture':
        return s['capture'](action=action, obj=obj)
    elif action_type.name is 'query_all':
        return s['query_all'](action=action, obj=obj)
    elif action_type.name is 'query':
        return s['query'](action=action, obj=obj, **status)
