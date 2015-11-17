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

from thirdparty import yaml


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
            raise AttributeError("object dose not have attribute '{0}'".format(key))

    def __setattr__(self, key, value):
        self[key] = value


class Log(object):
    '''
    critical, error, warning, info, debug, notset
    '''
    def __new__(cls, logname=None):
        if not logname:
            log = logging.getLogger('wiper')
            log.setLevel(logging.DEBUG)

            streamHD = logging.StreamHandler()
            streamHD.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
            streamHD.setFormatter(formatter)

            fileName = os.path.join("log","wiper.log")
            if not os.path.exists(fileName):
                with open(fileName,"w") as fd:
                    fd.write("global log start----------------\r\n")
            fileHD = logging.FileHandler(fileName)
            fileHD.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
            fileHD.setFormatter(formatter)

            log.addHandler(streamHD)
            log.addHandler(fileHD)
        else:
            log = logging.getLogger(logname)
            log.setLevel(logging.DEBUG)

            fileName = os.path.join('log', '{0}.log'.format(logname))
            if not os.path.exists(fileName):
                with open(fileName,"w") as fd:
                    fd.write("{0} log start----------------\r\n".format(logname))
            fileHD = logging.FileHandler(fileName)
            fileHD.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
            fileHD.setFormatter(formatter)

            log.addHandler(fileHD)

        return log


class Config(Dict):
    _confFile = os.path.join("data","config.yaml")

    def __init__(self):
        confFile = self._confFile
        if not os.path.exists(confFile):
            confFile = os.path.join("data","config.sample.yaml")
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

        super(Config,self).__init__(**confDict)


    def save(self):
        result = dict(**self)
        for key, value in result.iteritems():
            if isinstance(value, Dict):
                result[key] = dict(value)
        try:
            with open(self._confFile,'w') as fd:
                yaml.dump(result, fd, default_flow_style=False)
        except IOError:
            raise WIPError("write configure file '{0}' error".format(confFile))


class RuntimeData(Dict):
    def __init__(self, **kwargs):
        self.log = Log()

        super(RuntimeData, self).__init__(**kwargs)


CONF = Config()
#global var rtd, record the run time datas
RTD = RuntimeData()


