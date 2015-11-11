#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import sys
import time

import sqlite3 as mdb

from config import CONF, RTD, WIPError


class DBError(WIPError):
    def __init__(self, reason):
        self.errMsg = "DBError. " + ("reason: "+reason if reason else "")

    def __str__(self):
        return self.errMsg


def escapeString(strValue):
    escapeDict = {"'":"\\'", "\"":"\\\"", "\\":"\\\\", "\x00":"0"}
    return "".join([escapeDict.get(x, x) for x in strValue])


class DBManage(object):
    '''
    Manage the information database.
    '''

    def __init__(self,dbname=None,retry=3):
        #'raw' False: select default db, True: select default db
        self.__con = None
        self.__cur = None
        self.__retry = retry+1
        self.__dbname = dbname if dbname else CONF.db.name
        self.__db = os.path.join("data", self.__dbname)

        self.connect()


    def connect(self):
        '''
        Connect to database, if failed retrys
        '''
        success = True
        for i in xrange(self.__retry):
            success = True
            try:
                self.__con = mdb.connect(self.__db)
            except mdb.Error as error:
                #Could not connect the server, retrys
                time.sleep(i*2)
                continue
            else:
                break

        if not success:
            #RTD.log.error("DBError, cannot connect to the database, reason:{0}".format(str(error)))
            raise DBError("cannot connect to the server.")
        
        self.__con.row_factory = mdb.Row
        self.__cur = self.__con.cursor()

        return True


    def sql(self, sqlcmd):
        '''
        Execute SQL command.
        '''
        try:
            self.__cur.execute(sqlcmd)
            self.__con.commit()
        except mdb.Error as error:
            # failed, retry one time
            try:
                self.connect()
                self.__cur.execute(sqlcmd)
                self.__con.commit()
            except mdb.Error as error:
                #RTD.log.error("DBError, sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
                raise DBError("sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
        
        return True


    def query(self, sqlcmd):
        '''
        Query database.
        Returns:
            a dict list contains the query result, for example [{'id':1,'name':'hah'},{'id':2,'name':'wa'}]
        '''
        try:
            self.__cur.execute(sqlcmd)
        except mdb.Error as error:
            # failed, retry one time
            try:
                self.connect()
                self.__cur.execute(sqlcmd)
                self.__con.commit()
            except mdb.Error as error:
                #RTD.log.error("DBError, sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
                raise DBError("sql command '{0}' executing error, '{1}'".format(sqlcmd, error))

        #return a list of dict, likes [{'age': 42, 'name': u'John'}, {'age': 43, 'name': u'Alice'}]
        return [dict(zip(x.keys(),x)) for x in self.__cur]


    def close(self):
        if self.__con:
            self.__con.close()
            self.__con = None
            self.__cur = None

    def __enter__(self):
        return self

    def __exit__(self, *unuse):
        self.close()


class SQLQuery:
    '''
    Query database.
    Usage: 'with SQLQuery(sqlCmd) as result: pass'
    '''
    def __init__(self, sqlCmd):
        self.__sqlCmd = sqlCmd
        self.__db = DBManage()

    def __enter__(self):
        return self.__db.query(self.__sqlCmd)

    def __exit__(self, *unuse):
        if self.__db:
            self.__db.close()


class SQLExec:
    '''
    Execute SQL command.
    Usage: 'with SQLExec(sqlCmd) as result:pass'
    '''
    def __init__(self, sqlCmd, raw=False):
        self.__sqlCmd = sqlCmd
        self.__db = DBManage(raw=raw)

    def __enter__(self):
        return self.__db.sql(self.__sqlCmd)

    def __exit__(self, *unuse):
        if self.__db:
            self.__db.close()




