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


def initLog():
    '''
    critical, error, warning, info, debug, notset
    '''
    log = logging.getLogger('wip')
    log.setLevel(logging.DEBUG)

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


class Conf:
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        try:
            cf.read(os.path.join("app.config"))
            self.dbhost = cf.get("db", "db_host")
            self.dbport = cf.get("db", "db_port")
            self.dbuser = cf.get("db", "db_user")
            self.dbpassword = cf.get("db", "db_password")
            self.dbname = cf.get("db", "db_name")

            self.dnsServers = [x.strip() for x in cf.get("dns", "servers").split()]
            self.dnsTimeout = float(cf.get("dns", "timeout"))
        except ConfigParser.Error as msg:
            log.error("Read configure file failed, reason:{0}!".format(msg))
            exit(1)


if not os.path.exists("log"):
    os.mkdir("log")

if not os.path.exists(os.path.join("static","attachment")):
    os.mkdir(os.path.join("static","attachment"))


log = initLog()
conf = Conf()
conf.log = log


