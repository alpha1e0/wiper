#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import MySQLdb as mdb


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


if __name__ == "__main__":

	resetDatabase("wip", "localhost", "root", "86@shiyan")

