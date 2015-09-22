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


class DBError(Exception):
    def __init__(self, errorMsg):
        super(DBError, self).__init__()
        self.errorMsg = errorMsg

    def __str__(self):
        return self.errorMsg


mysqlCmdList = []
sqliteCmdList = []

mysqlCmdList.append("drop database {0}")
mysqlCmdList.append("create database {0}")
mysqlCmdList.append('''create table project (
    id integer not null auto_increment,
    name varchar(100) not null unique,
    url varchar(100), 
    ip varchar(50), 
    whois text, 
    ctime timestamp not null default CURRENT_TIMESTAMP,
    description text,
    primary key (id)
) engine=InnoDB  default charset=utf8;''')

mysqlCmdList.append('''create table host (
    id integer not null auto_increment, 
    title varchar(200) not null unique,
    url varchar(100), 
    ip varchar(50),
    protocol integer not null,
    level integer, 
    os varchar(150), 
    server_info varchar(150),
    middleware varchar(200), 
    description text, 
    project_id integer not null,
    unique key ipurl (ip, url),
    primary key (id),
    constraint project_id_host foreign key (project_id) references project (id)
) engine=InnoDB  default charset=utf8;''')

mysqlCmdList.append('''create table vul (
    id integer not null auto_increment, 
    name varchar(100), 
    url varchar(4096),
    info varchar(1024), 
    type integer, 
    level integer, 
    description text, 
    host_id integer not null, 
    primary key (id),
    constraint host_id_vul foreign key (host_id) references host (id)
) engine=InnoDB  default charset=utf8;''')

mysqlCmdList.append('''create table comment (
    id integer not null auto_increment, 
    name varchar(100), 
    url varchar(4096),
    info varchar(1024), 
    level integer, 
    attachment varchar(200),
    description text, 
    host_id integer not null, 
    primary key (id),
    constraint host_id_comment foreign key (host_id) references host (id)
) engine=InnoDB  default charset=utf8;''')

mysqlCmdList.append('''create table tmp_host (
    id integer not null auto_increment,
    title varchar(200) not null unique,
    url varchar(100), 
    ip varchar(50),
    protocol integer not null,
    level integer,
    os varchar(150), 
    server_info varchar(150),
    middleware varchar(200),
    project_id integer not null,
    source varchar(50),
    primary key (id),
    constraint project_id_tmp foreign key (project_id) references project (id)
) engine=InnoDB  default charset=utf8;''')



def createDatabase(dbname, dbhost, dbuser, dbpass, dbport=3306, dbtype="mysql"):
    if dbtype == "mysql":
        try:
            con = mdb.connect(host=dbhost, user=dbuser, passwd=dbpass, port=dbport, charset='utf8')
            cur = con.cursor()
        except mdb.Error as msg:
            print msg
            exit(1)

        try:
            cur.execute(mysqlCmdList[1].format(dbname))
        except mdb.Error as msg:
            print msg
            exit(1)

        con.select_db(dbname)

        try:
            for cmd in mysqlCmdList[2:]:
                cur.execute(cmd)
        except mdb.Error as msg:
            print msg
            exit(1)

def resetDatabase(dbname, dbhost, dbuser, dbpass, dbport=3306, dbtype="mysql"):
    if dbtype == "mysql":
        try:
            con = mdb.connect(host=dbhost, user=dbuser, passwd=dbpass, port=dbport, charset='utf8')
            cur = con.cursor()
        except mdb.Error as msg:
            print msg
            exit(1)

        try:
            cur.execute(mysqlCmdList[0].format(dbname))
            cur.execute(mysqlCmdList[1].format(dbname))
        except mdb.Error as msg:
            print msg
            exit(1)

        con.select_db(dbname)

        try:
            for cmd in mysqlCmdList[2:]:
                cur.execute(cmd)
        except mdb.Error as msg:
            print msg
            exit(1)


def escapeString(strValue):
    if isinstance(strValue, str):
        return mdb.escape_string(strValue)
    else:
        return ""


class DBManage(object):
    '''
    Manage the information database.
    '''

    def __init__(self,dbhost=None,dbuser=None,dbpassword=None,dbname=None,dbport=3306,retry=3):
        self.__con = None
        self.__cur = None
        self.__retry = retry+1

        self.dbhost = dbhost if dbhost else conf.dbhost
        self.dbuser = dbuser if dbuser else conf.dbuser
        self.dbpassword = dbpassword if dbpassword else conf.dbpassword
        self.dbname = dbname if dbname else conf.dbname
        self.dbport = dbport if dbport else conf.dbport

        self.connect()


    def connect(self):
        '''
        Connect to database, if failed retrys
        '''
        success = True
        for i in range(1,self.__retry):
            success = True
            try:
                self.__con = mdb.connect(host=self.dbhost, user=self.dbuser, passwd=self.dbpassword, db=self.dbname, charset='utf8')                
            except mdb.OperationalError as msg:
                #Could not connect the server, retrys
                if msg[0] == 2003: 
                    success = False
                    time.sleep(i*2)
                    continue
                elif msg[0] == 1045:
                    raise DBError("Database connect error, reason: user or password error.")
                elif msg[0] == 1049:
                    raise DBError("Database connect error, reason: database not exists.")
            else:
                break

        if not success:
            raise DBError("Database connect error, reason: cannot connect to the server, the server maybe down.")

        self.__cur = self.__con.cursor()
        return True


    def sql(self, sqlcmd):
        '''
        Execute SQL command.
        '''
        try:
            self.__cur.execute(sqlcmd)
            self.__con.commit()
        except mdb.OperationalError as msg:
            # if lost connection, retry one time
            if msg[0] == 2013:
                try:
                    self.connect()
                    self.__cur.execute(sqlcmd)
                    self.__con.commit()
                except mdb.OperationalError as msg:
                    raise DBError("SQL executing error, location: {0}, reason: {1}."format(sqlcmd, msg))
            else:
                raise DBError("SQL executing error, location: {0}, reason: {1}."format(sqlcmd, msg))
        except mdb.MySQLError as msg:
            raise DBError("SQL executing error, location: {0}, reason: {1}."format(sqlcmd, msg))
        
        return True


    def find(self, sqlcmd):
        '''
        Query database.
        Returns:
            a dict list contains the query result, for example [{'id':1,'name':'hah'},{'id':2,'name':'wa'}]
        '''
        try:
            self.__cur.execute(sqlcmd)
        except mdb.OperationalError as msg:
            # if lost connection, retry one time
            if msg[0] == 2013:
                try:
                    self.connect()
                    self.__cur.execute(sqlcmd)
                    self.__con.commit()
                except mdb.OperationalError as msg:
                    raise DBError("SQL executing error, location: {0}, reason: {1}."format(sqlcmd, msg))
            else: 
                raise DBError("SQL executing error, location: {0}, reason: {1}."format(sqlcmd, msg))
        except mdb.MySQLError as msg:
            raise DBError("SQL executing error, location: {0}, reason: {1}."format(sqlcmd, msg))

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

    def __exit__(self):
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
        return self.__db.find(self.__sqlCmd)

    def __exit__(self, *unuse):
        if self.__db:
            self.__db.close()

class SQLExec:
    '''
    Execute SQL command.
    Usage: 'with SQLExec(sqlCmd) as result:pass'
    '''
    def __init__(self, sqlCmd):
        self.__sqlCmd = sqlCmd
        self.__db = DBManage()

    def __enter__(self):
        return self.__db.sql(self.__sqlCmd)

    def __exit__(self, *unuse):
        if self.__db:
            self.__db.close()




