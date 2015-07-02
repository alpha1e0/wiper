#!/usr/bin/env python

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import sys
import sqlite3 as sqlite
from config import conf,log

class DBManage(object):
    '''
    Manage the information database
    '''

    def __init__(self):
        self.con = None
        self.cur = None
        self.connect()

    def connect(self):
        try:
            self.con = mdb.connect(host='localhost', user='root', passwd='86@shiyan', db='wip', charset='utf8')
            self.cur = self.con.cursor()
        except mdb.Error as msg:
            log.error("[E]: Connect failed, reason is {0}".format(msg))
            sys.exit(1)




