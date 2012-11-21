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
    ('query', u'查询'),

    ('TV2', u'电视'), ('TV2', u'电视机'),
    ('aircondictioner', u'空调'), ('aircondictionoar', u'冷气机'),
    ('A1', 'A1'),

    ('hours', u'小时'), ('hour', u'小时'), ('hr', u'小时'),
    ('minutes', u'分钟'), ('minute', u'分钟'), ('min', u'分钟'),
    ('seconds', u'秒'), ('second', u'秒'), ('sec', u'秒'),

    ('power', u'功率'),
))

ch_d = en_d.reverse()

action_type_d = Dict((
    ('turnon', 0), ('turnoff', 0),
    ('query', 1)
))


#: some sentence builders


def job_ok(*args, **kwargs):
    return u'OK啦！'


def job_failure(*args, **kwargs):
    return u'出问题啦！！！！！！1 你家的%s不能%s！' % (
                        kwargs['obj'], kwargs['action'])


def query(*args, **kwargs):
    # TODO translating
    basic = u'截至%s，你家的 %s:' % (
            datetime.utcnow().strftime(datetime_format),
            kwargs['obj']
            )

    # work duration
    desc = ''
    for eng in ('hours', 'minutes', 'seconds'):
        if eng in kwargs.keys():
            desc = desc or u'工作了'
            desc += ' %s %d' % (en_d.get(eng)[0], kwargs[eng])
    desc += u'，'
    basic += desc

    # work status (e.g., power)
    for eng in ('power'):
        if eng in kwargs.keys():
            basic += u' %s是 %s，' % (en_d.get(eng)[0], kwargs[eng])

    return basic


def query_all(*args, **kwarsg):
    #: actually, we have a photo
    basic = u'截至%s' % datetime.utcnow().strftime(datetime_format)
    return basic


def unknown_command(*args, **kwargs):
    return u'我不懂你的意思……'


#: s for sentences
s = {
    'OK': job_ok,
    'FAILURE': job_failure,
    'query': query,
    'query_all': query_all,
    'unknowncommand': unknown_command
}


#: h for hard-coding
_query_all = ('query', 1, 'all', 0)
h_d = Dict((
    (u'家里的用电器怎样啦', _query_all),
    (u'检查家里的用电器情况', _query_all)
))
