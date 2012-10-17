#coding: utf-8

unknown = []


def in_queue(id):
    return id in unknown


def enqueue(id):
    unknown.append(id)
