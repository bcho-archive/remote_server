#coding: utf-8

'''
    dictionary
    ~~~~~~~~~~

    You can look up everythings from dictionary.
'''


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
        default = default or attr
        if not isinstance(default, list):
            default = [default]
        return super(Dict, self).get(attr, default)

    def reverse(self):
        name_value = []
        for name, items in self.items():
            for item in items:
                name_value.append((item, name))
        return Dict(name_value)

#: d for dictionary
en_d = Dict((
    ('turnoff', u'关闭'), ('turnoff', u'关'),
    ('turnon', u'打开'), ('turnon', u'开'),

    ('tv', u'电视'), ('tv', u'电视机'),
    ('aircondictioner', u'空调'), ('aircondictionoar', u'冷气机'),

    ('hours', u'小时'), ('hour', u'小时'), ('hr', u'小时'),
    ('minutes', u'分钟'), ('minute', u'分钟'), ('min', u'分钟'),
    ('seconds', u'秒'), ('second', u'秒'), ('sec', u'秒')
))

ch_d = en_d.reverse()


#: some sentence builders


def job_ok(*args, **kwargs):
    return u'OK啦！'


def job_failure(*args, **kwargs):
    return u'出问题啦！！！！！！1 你家的%s不能%s！' % (
                        kwargs['obj'], kwargs['action'])


def works_duration(*args, **kwargs):
    basic = u'你家的%s已经工作' % (kwargs['obj'])
    for eng in ('hours', 'minutes', 'seconds'):
        if eng in kwargs.keys():
            basic += ' %d %s' % (kwargs[eng], en_d.get(eng)[0])
    return basic + u'了'

#: s for sentences
s = {
    'OK': job_ok,
    'FAILURE': job_failure,
    'works_duration': works_duration
}
