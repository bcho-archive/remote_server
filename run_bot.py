#coding: utf-8

from time import sleep

from server.weibot import bot


while True:
    bot.fetch()
    bot.send()
    sleep(2)
