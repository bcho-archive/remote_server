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

    def get(self, attr, default=None):
        # when self[name] is not found, return name
        # instead of None
        default = default or attr
        return super(Dict, self).get(attr, default)

    def reverse(self):
        name_value = []
        for name, items in self.items():
            for item in items:
                name_value.append((item, name))
        return Dict(name_value)

#: d for dictionary
en_d = Dict((
    ('turnoff', u'关闭'), ('turnon', u'打开'),
    ('turnon', u'开')
))

ch_d = en_d.reverse()


def job_ok(*args, **kwargs):
    return u'OK啦！'


def job_failure(*args, **kwargs):
    return u'出问题啦！！！！！！1 %s 不能 %s！' % (
                        kwargs['obj'], kwargs['action'])

#: s for sentences
s = {
    'OK': job_ok,
    'FAILURE': job_failure
}
