#coding: utf-8

from .dictionary import en_d as d
from .dictionary import s


def machine2human(report):
    action, obj = d.get(report['action'])[0], d.get(report['obj'])[0]
    status, action_type = report['status'], report['type']

    if action_type == 0:
        return s[status](action=action, obj=obj)

    if action_type == 1:
        return status
