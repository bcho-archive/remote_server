#coding: utf-8

from server.translator import human2machine as h


def repl():
    raw = raw_input('> ')
    print h(raw)


while True:
    repl()
