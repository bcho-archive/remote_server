#coding: utf-8

from random import random


class Box(dict):

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


def random_id():
    '''generate a 13-digits integer'''
    return int(random() * 10 ** 13)
