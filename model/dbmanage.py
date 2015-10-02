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

import MySQLdb as mdb

from init import conf, log, WIPError


class DBError(WIPError):
    def __init__(self, reason):
        self.errMsg = "DBError. " + ("reason: "+reason if reason else "")

    def __str__(self):
        return self.errMsg


def escapeString(strValue):
    if isinstance(strValue, basestring):
        return mdb.escape_string(strValue)
    else:
        return ""


class DBManage(object):
    '''
    Manage the information database.
    '''

    def __init__(self,dbhost=None,dbuser=None,dbpassword=None,dbname=None,dbport=3306,retry=3,raw=False):
        #'raw' means connect the database with or without dbname.
        self.__con = None
        self.__cur = None
        self.__retry = retry+1

        self.dbhost = dbhost if dbhost else conf.dbhost
        self.dbuser = dbuser if dbuser else conf.dbuser
        self.dbpassword = dbpassword if dbpassword else conf.dbpassword
        self.dbname = dbname if dbname else conf.dbname
        self.dbport = dbport if dbport else conf.dbport

        self.raw = raw
        self.connect()


    def connect(self):
        '''
        Connect to database, if failed retrys
        '''
        success = True
        for i in range(1,self.__retry):
            success = True
            try:
                self.__con = mdb.connect(host=self.dbhost, user=self.dbuser, passwd=self.dbpassword, charset='utf8')
                if not self.raw:
                    self.__con.select_db(self.dbname)
            except mdb.OperationalError as error:
                #Could not connect the server, retrys
                if error[0] == 2003: 
                    success = False
                    time.sleep(i*2)
                    continue
                elif error[0] == 1045:
                    log.error("DBError, cannot connect to the database server, user or password error.")
                    raise DBError("user or password error")
                elif error[0] == 1049:
                    log.error("DBError, cannot connect to the database server, database not exists.")
                    raise DBError("database not exists")
            else:
                break

        if not success:
            log.error("DBError, cannot connect to the database server, the server maybe down.")
            raise DBError("cannot connect to the server, the server maybe down.")

        self.__cur = self.__con.cursor()
        return True


    def sql(self, sqlcmd):
        '''
        Execute SQL command.
        '''
        try:
            self.__cur.execute(sqlcmd)
            self.__con.commit()
        except mdb.OperationalError as error:
            # if lost connection, retry one time
            if error[0] == 2013:
                try:
                    self.connect()
                    self.__cur.execute(sqlcmd)
                    self.__con.commit()
                except mdb.OperationalError as error:
                    log.error("DBError, sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
                    raise DBError("sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
            else:
                log.error("DBError, sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
                raise DBError("sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
        except mdb.MySQLError as error:
            log.error("DBError, sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
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
        except mdb.OperationalError as error:
            # if lost connection, retry one time
            if error[0] == 2013:
                try:
                    self.connect()
                    self.__cur.execute(sqlcmd)
                    self.__con.commit()
                except mdb.OperationalError as error:
                    log.error("DBError, sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
                    raise DBError("sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
            else:
                log.error("DBError, sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
                raise DBError("sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
        except mdb.MySQLError as error:
            log.error("DBError, sql command '{0}' executing error, '{1}'".format(sqlcmd, error))
            raise DBError("sql command '{0}' executing error, '{1}'".format(sqlcmd, error))

        nameList = [x[0] for x in self.__cur.description]
        result = [dict(zip(nameList,x)) for x in self.__cur.fetchall()]
            
        return result


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




