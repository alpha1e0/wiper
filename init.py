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
import ConfigParser

import yaml

from  plugin.lib.taskmanager import TaskManager

reload(sys)
sys.setdefaultencoding("utf-8")


class WIPError(Exception):
    def __init__(self, reason=""):
        self.errMsg = "WIPError. " + ("reason: "+reason if reason else "")

    def __str__(self):
        return self.errMsg


def Enum(**enums):
    return type('Enum', (), enums)


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


class Conf(object):
    def __init__(self):
        self._confFile = "config.yaml"

        confFile = self._confFile
        
        if not os.path.exists(confFile):
            confFile = "config.sample.yaml"
            if not os.path.exists(confFile):
                raise WIPError("cannot find configure file, 'config.yaml' or 'config.sample.yaml'")

        try:
            with open(confFile,'r') as fd:
                self._confDict = yaml.load(fd)
        except IOError:
            raise WIPError("open configure file '{0}' error".format(confFile))
        except yaml.scanner.ScannerError:
            raise WIPError("configure file '{0}' format error, should be yaml format".format(confFile))


    @property
    def dbhost(self):
        return self._confDict['db']['host']
    @dbhost.setter
    def dbhost(self, value):
        self._confDict['db']['host'] = value

    @property
    def dbport(self):
        return self._confDict['db']['port']
    @dbport.setter
    def dbport(self, value):
        self._confDict['db']['port'] = value

    @property
    def dbuser(self):
        return self._confDict['db']['user']
    @dbuser.setter
    def dbuser(self, value):
        self._confDict['db']['user'] = value

    @property
    def dbpassword(self):
        return self._confDict['db']['password']
    @dbpassword.setter
    def dbpassword(self, value):
        self._confDict['db']['password'] = value

    @property
    def dbname(self):
        return self._confDict['db']['name']
    @dbname.setter
    def dbname(self, value):
        self._confDict['db']['name'] = value
    
    @property
    def isinstall(self):
        return self._confDict['isinstall']
    @isinstall.setter
    def isinstall(self, value):
        self._confDict['isinstall'] = value

    @property
    def dnsServers(self):
        return self._confDict['dns']['servers']
    @dnsServers.setter
    def dnsServers(self, value):
        self._confDict['dns']['servers'] = value

    @property
    def dnsTimeout(self):
        return self._confDict['dns']['timeout']
    @dnsTimeout.setter
    def dnsTimeout(self, value):
        self._confDict['dns']['timeout'] = value

    
    def save(self):
        yaml.dump(self._confDict, self._confFile)



log = Log()
conf = Conf()
taskManager = TaskManager()
conf.log = log
conf.taskManager = taskManager
