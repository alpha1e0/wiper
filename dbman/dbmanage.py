#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import sys
import ConfigParser
import MySQLdb as mdb

from init import log

class DBManage(object):
    '''
    Manage the information database
    '''

    def __init__(self):
        self.con = None
        self.cur = None

        cf = ConfigParser.ConfigParser()
        cf.read("dbman/db.config")
        dbhost = cf.get("db", "db_host")
        dbuser = cf.get("db", "db_user")
        dbpassword = cf.get("db", "db_password")

        self.connect(dbhost, dbuser, dbpassword)


    def connect(self, dbhost, dbuser, dbpassword):
        try:
            self.con = mdb.connect(host=dbhost, user=dbuser, passwd=dbpassword, db='wip', charset='utf8')
            self.cur = self.con.cursor()
        except mdb.Error as msg:
            log.error("[E]: Connect failed, reason is {0}".format(msg))
            return False

        return True


    def sql(self, sqlcmd):
        try:
            self.cur.execute(sqlcmd)
            self.con.commit()
        except mdb.Error as msg:
            log.error("Execute sql cmmmand {0} failed, reason is {1}".format(sqlcmd, msg))
            return False
        
        return True


    def find(self, sqlcmd):
        try:
            self.cur.execute(sqlcmd)
        except mdb.Error as msg:
            log.error("Find failed, command is {0}, reason is {1}.".format(sqlcmd, msg))
            return False
            
        return self.cur.fetchall()



