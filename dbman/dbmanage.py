#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import sys
import time
import MySQLdb as mdb

from init import log
from init import conf


class DBManage(object):
    '''
    Manage the information database
    '''

    def __init__(self,dbhost=None,dbuser=None,dbpassword=None,dbname=None,retry=3):
        self.con = None
        self.cur = None
        self.retry = retry+1

        self.dbhost = dbhost if dbhost else conf.dbhost
        self.dbuser = dbuser if dbuser else conf.dbuser
        self.dbpassword = dbpassword if dbpassword else conf.dbpassword
        self.dbname = dbname if dbname else conf.dbname

        self.connect()


    def connect(self):
        '''
        Connect to database, if failed retrys
        '''
        success = 1
        for i in range(1,self.retry):
            success = 1
            try:
                self.con = mdb.connect(host=self.dbhost, user=self.dbuser, passwd=self.dbpassword, db=self.dbname, charset='utf8')                
            except mdb.Error as msg:
                if msg[0] == 2002: 
                    success = 0
                    time.sleep(i*2)
                    continue
            break

        if not success:
            log.error("Connect failed, reason is {0}".format(msg))
            exit(1)

        self.cur = self.con.cursor()

        return True


    def sql(self, sqlcmd):
        try:
            self.cur.execute(sqlcmd)
            self.con.commit()
        except mdb.Error as msg:
            if msg[0] == 2002:
                self.connect(dbhost, dbuser, dbpassword, 1)
                self.cur.execute(sqlcmd)
                self.con.commit()
            else:
                log.error("Execute sql cmmmand {0} failed, reason is {1}".format(sqlcmd, msg))
                return False
        
        return True


    def find(self, sqlcmd):
        try:
            self.cur.execute(sqlcmd)
        except mdb.Error as msg:
            if msg[0] == 2002:
                self.connect(dbhost, dbuser, dbpassword, 1)
                self.cur.execute(sqlcmd)
                self.con.commit()
            else:
                log.error("Execute sql cmmmand {0} failed, reason is {1}".format(sqlcmd, msg))
                return False
            
        return self.cur.fetchall()



