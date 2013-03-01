#coding: utf-8

'''
    dictionary
    ~~~~~~~~~~

    You can look up everythings from dictionary.
'''

from datetime import datetime

from server.config import datetime_format
from .action import Action


class MultiDict(dict):
    '''A dict obj which one key can have serval children.'''

    def __init__(self, kv=None):
        kv = kv or []
        for k, v in kv:
            if not super(MultiDict, self).get(k):
                self[k] = v
            else:
                self[k].append(v)

    def get(self, k, default=None):
        #: return [k] if k is not found.
        default = default or [k]
        if not isinstance(default, list):
            default = [default]
        return super(MultiDict, self).get(k, default)

    def __setitem__(self, k, v):
        if k not in self.keys():
            super(MultiDict, self).__setitem__(k, [v])
        else:
            self[k].append(v)

    def reverse(self):
        kv = []
        for k, v in self.items():
            for item in v:
                kv.append((item, k))
        return MultiDict(kv)


#: vocabulary labels
l_d = dict([
        ('noun', ['n', 'nr', 'ns', 'ng', 'eng']),
        ('time', ['t', 'tg']),
        ('verb', ['v', 'vd', 'vn', 'vf', 'vx', 'vi', 'vg']),
        ('adj', ['a', 'ad', 'an', 'ag', 'al']),
        ('num', ['m', 'mq']),
        ('measure', ['q', 'qv', 'qt'])
])

#: time convert helpers
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

#: dictionary
en_d = MultiDict([
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
])
ch_d = en_d.reverse()

#: actions defination
action_type_d = dict([
    ('turnon', Action('turnon', 0, 0, 1)),
    ('turnoff', Action('turnoff', 0, 0, 1)),
    ('query', Action('query', 1, 0, 1)),
    ('query_all', Action('query_all', 1, 1, 0)),
    ('capture', Action('capture', 1, 1, 0))
])

#: sentences
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
    # TODO test duration converting
    total_time = int(kwargs.get('time', 0))
    hours, total_time = total_time / 3600, total_time % 3600
    minutes, seconds = total_time / 60, total_time % 60
    desc = '工作了 %d %s %d %s %d %s' % (
        hours, en_d.get('hours'),
        minutes, en_d.get('minutes'),
        seconds, en_d.get('seconds')
    )
    basic += desc

    return basic

def query_all(*args, **kwargs):
    basic = u'截至%s' % datetime.utcnow().strftime(datetime_format)
    return basic


def capture(*args, **kwargs):
    return u'看！'


def unknown_command(*args, **kwargs):
    return u'我不懂你的意思……'


s = {
    'OK': job_ok,
    'FAILURE': job_failure,
    'query': query,
    'capture': capture,
    'query_all': query_all,
    'unknowncommand': unknown_command
}


#: some hard coding cases
_query_all = ('query', 1, 'all', 0)
h_d = MultiDict((
    (u'家里的用电器怎样啦', _query_all),
    (u'检查家里的用电器情况', _query_all)
))
