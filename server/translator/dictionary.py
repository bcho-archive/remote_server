#coding: utf-8

'''
    dictionary
    ~~~~~~~~~~

    You can look up everythings from dictionary.
'''

from datetime import datetime

from server.config import datetime_format


class Dict(dict):
    def __init__(self, name_value=None):
        for name, value in name_value:
            if not super(Dict, self).get(name):
                self[name] = [value]
            else:
                self[name].append(value)

    def get(self, attr, default=[]):
        # when self[name] is not found, return name
        # instead of None
        if not isinstance(default, list):
            default = [default]
        default = default or [attr]
        if not isinstance(default, list):
            default = [default]
        return super(Dict, self).get(attr, default)

    def reverse(self):
        name_value = []
        for name, items in self.items():
            for item in items:
                name_value.append((item, name))
        return Dict(name_value)


#: l for labels
l_d = {
        'noun': ['n', 'nr', 'ns', 'ng', 'eng'],
        'time': ['t', 'tg'],
        'verb': ['v', 'vd', 'vn', 'vf', 'vx', 'vi', 'vg'],
        'adj': ['a', 'ad', 'an', 'ag', 'al'],
        'num': ['m', 'mq'],
        'measure': ['q', 'qv', 'qt']
}

#: t for time convert helers
_h = lambda x: x * 3600
_m = lambda x: x * 60
_s = lambda x: x * 1
t_d = {
        'hour': _h,
        'hours': _h,
        'hr': _h,
        'minute': _m,
        'minutes': _m,
        'min': _m,
        'second': _s,
        'seconds': _s,
        'sec': _s
}

#: d for dictionary
en_d = Dict((
    ('turnoff', u'关闭'), ('turnoff', u'关'),
    ('turnon', u'打开'), ('turnon', u'开'),
    ('query', u'状态'), ('query', u'情况'), ('query', u'检查'),
    ('query', u'查询'), ('capture', u'拍照'),

    ('TV', u'电视'), ('TV', u'电视机'),
    ('air condition', u'空调'), ('air condition', u'冷气机'),
    ('balcony light', u'灯'),

    ('hours', u'小时'), ('hour', u'小时'), ('hr', u'小时'),
    ('minutes', u'分钟'), ('minute', u'分钟'), ('min', u'分钟'),
    ('seconds', u'秒'), ('second', u'秒'), ('sec', u'秒'),

    ('power', u'功率'),
))

ch_d = en_d.reverse()

#: 0 -- action 1 -- query action
action_type_d = Dict((
    ('turnon', 0), ('turnoff', 0),
    ('query', 1), ('capture', 0),
))


#: some sentence builders


def job_ok(*args, **kwargs):
    return u'OK啦！'


def job_failure(*args, **kwargs):
    return u'出问题啦！！！！！！1 你家的%s不能%s！' % (
                        kwargs['obj'], kwargs['action'])


def query(*args, **kwargs):
    # TODO translating
    basic = u'截至 %s，你家的 %s :' % (
            datetime.utcnow().strftime(datetime_format),
            kwargs['obj']
            )

    # work duration
    total_time = int(kwargs.get('time', 0))
    hours, total_time = total_time / 3600, total_time % 3600
    minutes, seconds = total_time / 60, total_time % 60
    desc = u'工作了 %d %s %d %s %d %s' % (
        hours, en_d.get('hours')[0],
        minutes, en_d.get('minutes')[0],
        seconds, en_d.get('seconds')[0]
    )
    basic += desc

    return basic


def query_all(*args, **kwargs):
    #: actually, we have a photo
    basic = u'截至%s' % datetime.utcnow().strftime(datetime_format)
    return basic


def capture(*args, **kwargs):
    return u'看！'


def unknown_command(*args, **kwargs):
    return u'我不懂你的意思……'

#: s for sentences
s = {
    'OK': job_ok,
    'FAILURE': job_failure,
    'query': query,
    'capture': capture,
    'query_all': query_all,
    'unknowncommand': unknown_command
}


#: h for hard-coding
_query_all = ('query', 1, 'all', 0)
h_d = Dict((
    (u'家里的用电器怎样啦', _query_all),
    (u'检查家里的用电器情况', _query_all),
    (u'开灯', ('turnon', 1, 'balcony light', 0)),
    (u'关灯', ('turnoff', 1, 'balcony light', 0))
))
