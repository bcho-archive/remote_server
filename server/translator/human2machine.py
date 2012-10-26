#coding: utf-8

import gkseg as seg

from server.base import logger
from dictionary import ch_d, type_d, action_type_d


# Buggy translating
#
# Short: this is a simple dictionary to translate the human order to machine
#        order, everything is hardcode.
#
# In order to translate the human sentence to machine order, we first do a
# language segment (currently using [gkseg](http://github/guokr/gkseg), slow
# but useful), to extract the important part. Then, we look up the word from
# our set dictionary (called `ch_d` here) and determain its type with another
# dictionary (called `type_d` here). Additonly, we use `action_type_d`
# dictionary to determain the action type.
#
# I know it's really hard-coding, buggy and useless, but NLP is not a easy
# task for me now...
def human2machine(msg):
    if not isinstance(msg, unicode):
        msg = msg.decode('utf-8')
    seg.init()

    action = None
    action_type = None
    obj = None
    repeated_duration = 0
    # FIXME if send a msg like '每30分钟检查一次空调'
    #       after the segment, it will be:
    #           [u'\u6bcf3', u'0', u'\u5206\u949f', u'\u68c0\u67e5', u'\u4e00',
    #            u'\u6b21', u'\u7a7a\u8c03']
    #       which is out our expected.
    for word in seg.term(msg):
        #: is it a repeated job?
        try:
            # TODO time unit determinations
            #      I just suppose all the repeat interval
            #      is **minute** base. But the arm side
            #      uses **second**.
            repeated_duration = int(word) * 60
        except ValueError:
            #: tranlate the word
            en = ch_d.get(word, None)[0]
            if en:
                word_type = type_d.get(en)[0]
                if word_type == 'action':
                    #: determin the action type
                    action_type, action = action_type_d.get(en)[0], en
                elif word_type == 'obj':
                    obj = en

    seg.destroy()

    if action and (action_type is not None) and obj:
        return action, action_type, obj, repeated_duration
    else:
        logger.info('Found unknown command %s' % msg)
        return None
