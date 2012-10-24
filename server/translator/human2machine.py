#coding: utf-8

import gkseg as seg

from server.base import logger
from dictionary import ch_d, type_d, action_type_d


def human2machine(msg):
    if not isinstance(msg, unicode):
        msg = msg.decode('utf-8')
    seg.init()

    action = None
    action_type = None
    obj = None
    for word in seg.term(msg):
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
        return action, action_type, obj
    else:
        logger.info('Found unknown command %s' % msg)
        return None
