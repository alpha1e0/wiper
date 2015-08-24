#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import sys
import logging

reload(sys)
sys.setdefaultencoding("utf-8")


def initLog():
    '''
    critical, error, warning, info, debug, notset
    '''
    log = logging.getLogger('wip')
    #log.setLevel(logging.DEBUG)

    streamHD = logging.StreamHandler()
    streamHD.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
    streamHD.setFormatter(formatter)

    fileHD = logging.FileHandler(os.path.join('log', 'wiplog.log'))
    fileHD.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
    fileHD.setFormatter(formatter)

    log.addHandler(streamHD)
    log.addHandler(fileHD)

    return log


if not os.path.exists("log"):
    os.mkdir("log")

if not os.path.exists("static/attachment"):
    os.mkdir("static/attachment")


log = initLog()


