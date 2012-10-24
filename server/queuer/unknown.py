#coding: utf-8

'''
    unknown
    ~~~~~~~
    Holding the unknown orders from the user.
'''

unknown = []


def in_queue(id):
    return id in unknown


def enqueue(id):
    unknown.append(id)
