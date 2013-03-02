#coding: utf-8

import logging

from server.config import unknown_command_log, log_format
from server.logger import get_file_logging_handler as file_logger
from server.logger import get_console_logging_handler as console_logger
from dictionary import ch_d, action_type_d, h_d, l_d, t_d


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format)
logger.addHandler(file_logger(formatter, log_path=unknown_command_log))
logger.addHandler(console_logger(formatter))


# Buggy translating
#
# Short: this is a simple dictionary to translate the human order to machine
#        order, everything is hard coded.
#
# In order to translate the human sentence to machine order, we first do a
# language segment (currently using [jieba](), slow but very useful), to
# seperate and flag the words. Then, we look up the word from our
# set dictionary (called `ch_d` here). Additonly, we use `action_type_d`
# dictionary to determain the action type.
#
# I know it's really hard-coded, buggy and useless, but NLP is not a easy
# task for me now...

def classify(words, required_flags=None):
    '''Classify the words basic on their flag'''
    required_flags = required_flags or []
    ret = dict.fromkeys(required_flags)
    for k in ret.keys():
        ret[k] = []
    for word in words:
        for k, v in l_d.items():
            if word.flag in v:
                ret[k].append(word.word)
                break
    for flag in set(ret.keys()) - set(required_flags):
        ret.pop(flag, None)
    return ret


def find_repeated(d):
    '''Find repeated duration'''
    if not d.get('num', None) or \
       not (d.get('measure', None) or d.get('noun', None)):
        return None

    basic, unit = None, None
    for n in d['num']:
        try:
            basic = int(n)
        except:
            pass
    for m in d.get('measure', []) + d.get('noun', []):
        unit = t_d.get(ch_d.get(m, None)[0], None) or unit
    if basic and unit:
        return unit(basic)
    return None


def human2machine(msg):
    if not isinstance(msg, unicode):
        msg = msg.decode('utf-8')

    #: process with some hard coded translations first
    for k, v in h_d.items():
        if msg in k:
            return v

    action = None
    action_type = None
    obj = None
    repeated_duration = 0

    import jieba.posseg as pseg
    seg = classify(pseg.cut(msg), l_d.keys())

    for v in seg['verb']:
        action = ch_d.get(v, None)[0]
    action = action or ''
    action_type = action_type_d.get(action, None)

    for n in seg['noun']:
        obj = ch_d.get(n, [None])[0] or obj

    repeated_duration = find_repeated(seg) or 0

    if action_type and action_type.validate(action, obj):
        return action, obj, repeated_duration
    else:
        logger.debug('Found unknown command %s: <%s, %s, %s>' % \
                (msg, action, obj, str(repeated_duration)))
        logger.debug('Seg: %s' % (seg))
        return None
