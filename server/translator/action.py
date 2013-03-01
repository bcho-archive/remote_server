#coding: utf-8

'''
action.py
~~~~~~~~~
Declares action model
'''

class Action(object):
    def __init__(self, name, can_repeated, can_with_pic, with_obj):
        self.name = name
        self.can_repeated = can_repeated
        self.can_with_pic = can_with_pic
        self.with_obj = with_obj

    def validate(self, name, obj):
        if name != self.name:
            return False
        # if the action declared without obj,
        # and still found the obj in the command,
        # also assume it's validated.
        if self.with_obj and not obj:
            return False
        return True
