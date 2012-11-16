#coding: utf-8

from time import sleep
from sys import argv

from server.weibot import bot
from server.tester.run import run


if argv[-1] == 'testing':
    run(10)
else:
    while True:
        bot.fetch()
        bot.send()
        sleep(2)
