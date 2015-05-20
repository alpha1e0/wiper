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

    def __init__(self, project):
        self.dbpath = os.path.join(project.projectPath, 'info.db')
        self.con = None
        self.cur = None

    def createDB(self):
        try:
            self.con = sqlite.connect(self.dbpath)
        except sqlite.Error as msg:
            log.error('Cannot database failed, reason:{0}'.format(msg))
            sys.exit(1)
        
        tableNetworkCmd = "create table if not exist network(id integer not null auto_increment, project nchar(100), url nchar(100), ip nchar(50), whois text, description text)"
        tableSiteCmd = "create table if not exist site(id integer not null auto_increment, url nchar(100), ip nchar(50), level integer, server nchar(100), x-powered nchar(100), framework nchar(100), description text, net_id integer, constraint net_id foreign key reference network (id))"
        tablePortCmd = "create table if not exist port(id integer not null auto_increment, port int, app nchar(100), version nchar(100), level integer, description text, site_id integer, constraint site_id foreign key reference site (id))"
        tableVulCmd = "create table if not exist vul(id integer not null auto_increment, vul nchar(50), point nchar(1024), type integer, levle integer, description text, site_id integer, port_id integer, constraint site_id foreign key reference site (id), constraint port_id foreign key reference port (id))"
        tableCommentCmd = "create table if not exist comment(id integer not null auto_increment, point nchar(1024), level integer, comment text, site_id integer, port_id integer, constraint site_id foreign key reference site (id), constraint port_id foreign key reference port (id))"
    
        try:
            self.con.execute(tableNetworkCmd)
            self.con.execute(tableSiteCmd)
            self.con.execute(tablePortCmd)
            self.con.execute(tableVulCmd)
            self.con.execute(tableCommentCmd)
            self.con.commit()
        except sqlite.Error as msg:
            log.error('Create table faild, reason:{0}'.format(msg))
            sys.exit(1)


