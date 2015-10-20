#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import sys
import logging

import yaml

#from  plugin.lib.taskmanager import TaskManager

reload(sys)
sys.setdefaultencoding("utf-8")


class WIPError(Exception):
    def __init__(self, reason=""):
        self.errMsg = "WIPError. " + ("reason: "+reason if reason else "")

    def __str__(self):
        return self.errMsg


class Dict(dict):
    def __init__(self, **kwargs):
        super(Dict, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("object has no attribute '{0}'".format(key))

    def __setattr__(self, key, value):
        self[key] = value


class Log(object):
    '''
    critical, error, warning, info, debug, notset
    '''
    def __new__(cls, logfile=None):
        if not logfile:
            log = logging.getLogger('wip')
            log.setLevel(logging.DEBUG)

            streamHD = logging.StreamHandler()
            streamHD.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
            streamHD.setFormatter(formatter)

            fileHD = logging.FileHandler(os.path.join('log', 'wiplog.log'))
            fileHD.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
            fileHD.setFormatter(formatter)

            log.addHandler(streamHD)
            log.addHandler(fileHD)
        else:
            fileHD = logging.FileHandler(os.path.join('log', '{0}.log'.format(logfile)))
            fileHD.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
            fileHD.setFormatter(formatter)

            log.addHandler(fileHD)

        return log


class Conf(Dict):
    _confFile = "config.yaml"

    def __init__(self):
        confFile = self._confFile
        if not os.path.exists(confFile):
            confFile = "config.sample.yaml"
            if not os.path.exists(confFile):
                raise WIPError("cannot find configure file, 'config.yaml' or 'config.sample.yaml'")

        try:
            with open(confFile,'r') as fd:
                confDict = yaml.load(fd)
        except IOError:
            raise WIPError("open configure file '{0}' error".format(confFile))
        except yaml.scanner.ScannerError:
            raise WIPError("configure file '{0}' format error, should be yaml format".format(confFile))

        for key,value in confDict.iteritems():
            if isinstance(value, dict):
                confDict[key] = Dict(**value)

        super(Conf, self).__init__(**confDict)


    def save(self):
        try:
            with open(self._confFile,'w') as fd:
                yaml.dump(self, fd)
        except IOError:
            raise WIPError("write configure file '{0}' error".format(confFile))


conf = Conf()

#global var rtd, record the run time datas
rtd = Dict()
log = Log()
rtd.log = log

