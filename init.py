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


reload(sys)
sys.setdefaultencoding("utf-8")

class WIPError(Exception):
    def __init__(self, reason=""):
        self.errMsg = "WIPError. " + ("reason: "+reason if reason else "")

    def __str__(self):
        return self.errMsg


def Enum(**enums):
    return type('Enum', (), enums)


def genLog(logfile=None):
    '''
    critical, error, warning, info, debug, notset
    '''
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


class Conf:
    def __init__(self):
        self._configFile = "app.config"
        self._cf = ConfigParser.ConfigParser()
        self.read()

    @property
    def configFile(self):
        return self._configFile

    @configFile.setter
    def configFile(self, value):
        self._configFile = value.strip()
    

    def read(self):
        '''
        Read the configure file, get the configuration.
        '''
        try:
            self._cf.read(os.path.join(self._configFile))
            self.dbhost = self._cf.get("db", "db_host")
            self.dbport = self._cf.get("db", "db_port")
            self.dbuser = self._cf.get("db", "db_user")
            self.dbpassword = self._cf.get("db", "db_password")
            self.dbname = self._cf.get("db", "db_name")

            self.dnsServers = [x.strip() for x in self._cf.get("dns", "servers").split()]
            self.dnsTimeout = float(self._cf.get("dns", "timeout"))
        except ConfigParser.Error as msg:
            log.error("Read configure file failed, reason:{0}!".format(msg))
            raise WIPError("read configure file error")


    def set(self, section, option, value):
        '''
        Set a configure.
        '''
        try:
            self._cf.set(section, option, value)
        except ConfigParser.Error as msg:
            log.error("Set configure failed, reason:{0}!".format(msg))
            raise WIPError("set configure error")
        

    def write(self):
        '''
        Write configures to configure file.
        '''
        try:
            with open(self._configFile, "w") as fd:
                self._cf.write(fd)
        except IOError as msg:
            log.error("Write configure file failed, reason:{0}!".format(msg))
            raise WIPError("write configure file error")


if not os.path.exists("log"):
    os.mkdir("log")

if not os.path.exists(os.path.join("static","attachment")):
    os.mkdir(os.path.join("static","attachment"))


log = genLog()
conf = Conf()
conf.log = log

log.debug("init application ================================================= ")

