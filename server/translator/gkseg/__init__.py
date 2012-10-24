#!/usr/bin/env python
# -*- coding: utf-8 -*-

from segment.crf import seg as crfseg
from segment.crf import init as crfinit
from segment.crf import destroy as crfdestroy

def init(model=None):
    crfinit(model)

def process(text, countErr=False):
    return crfseg(text, countErr)

def seg(text):
    return crfseg(text)[0]

def term(text):
    return crfseg(text)[1]

def label(text):
    return crfseg(text)[2]

def destroy():
    crfdestroy()

