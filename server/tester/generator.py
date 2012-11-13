#coding: utf-8

'''
    generator
    ~~~~~~~~~

    For generating some test data
'''

from server.config import tester as g
from .utils import Box, random_id


def build_tweet(text):
    '''build a tweet which contains id, name and text'''
    return Box(id=random_id(), name=g['id'], text=text)


def tweets():
    '''generate a bunch of tweets'''
    with open(g['raw'], 'r') as fn:
        l = []
        for c in fn.readlines():
            l.append(build_tweet(c.decode('utf-8')))
    return l
