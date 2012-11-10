#coding: utf-8

'''
    imagesbin
    ~~~~~~~~~

    For handling images.
'''

from os.path import join

from server.config import image_path


def get(name):
    '''get an image filehandler basic on name'''
    abspath = join(image_path, '%s.png' % (name))
    try:
        return file(abspath)
    except IOError:
        return None


def save(name, stream):
    abspath = join(image_path, '%s.png' % (name))
    stream.save(abspath)
