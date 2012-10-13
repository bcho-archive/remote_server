#coding: utf-8

from time import sleep

from server.weibot import report


while True:
    report.fetch()
    report.send()
    sleep(2)
