#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os

from orm import Model, IntegerField, StringField, UrlField, IPField, TextField, BooleanField, ModelError
from config import CONF


class Project(Model):
    _table = "project"

    id = IntegerField(primarykey=True,notnull=True,ddl="integer")
    name = StringField(notnull=True,ddl="varchar(100)",vrange="1-100")
    url = UrlField(ddl="varchar(100)")
    ip = IPField(ddl="varchar(50)")
    level = IntegerField(notnul=True,ddl="integer",vrange="1-4")
    ctime = StringField(ddl="date")
    whois = TextField(ddl="text")
    description = TextField(ddl="text")


    def __eq__(self, other):
        if not isinstance(other,Project):
            raise ModelError("the right instance is not Project")

        return self.getVal('name') == other.getVal('name')


    @classmethod
    def create(cls):
        sqlCmd = ("create table if not exists project("
            "id integer primary key autoincrement,"
            "name varchar(100) not null unique,"
            "url varchar(100),"
            "ip varchar(50),"
            "level integer,"
            "whois text,"
            "ctime date default (datetime('now','localtime')),"
            "description text"
            ")")
        cls.sqlexec(sqlCmd)


class Host(Model):
    _table = "host"

    id = IntegerField(primarykey=True,notnull=True,ddl="integer")
    title = StringField(ddl="varchar(100)",vrange="0-100")
    url = UrlField(ddl="varchar(100)")
    ip = IPField(ddl="varchar(50)")
    port = IntegerField(ddl="integer",vrange="1-65535")
    protocol = StringField(notnull=True,ddl="varchar(30)",vrange="1-30")
    level = IntegerField(notnul=True,ddl="integer",vrange="1-4",default=3)
    os = StringField(ddl="varchar(150)",vrange="0-150")
    server_info = StringField(ddl="varchar(150)",vrange="0-150")
    middleware = StringField(ddl="varchar(200)",vrange="0-200")
    description = TextField(ddl="text")
    tmp = IntegerField(ddl="integer",vrange="0-1",default=0)
    project_id = IntegerField(notnull=True,ddl="integer")


    def __eq__(self, other):
        if not isinstance(other,Host):
            raise ModelError("the right instance is not Host")

        if self.getVal('ip')==other.getVal('ip') and \
            self.getVal('url')==other.getVal('url') and \
            self.getVal('port')==other.getVal('port'):
            return True
        else:
            return False


    @classmethod
    def create(cls):
        sqlCmd = ("create table if not exists host ("
            "id integer primary key autoincrement,"
            "title varchar(200),"
            "url varchar(100),"
            "ip varchar(50),"
            "port integer,"
            "protocol varchar(30) not null,"
            "level integer not null default 3,"
            "os varchar(150),"
            "server_info varchar(150),"
            "middleware varchar(200),"
            "description text,"
            "tmp integer not null default 0,"
            "project_id integer not null,"
            "unique (ip, url, port) on conflict replace,"
            "foreign key (project_id) references project (id)"
            ")")
        cls.sqlexec(sqlCmd)


class Vul(Model):
    _table = "vul"

    id = IntegerField(primarykey=True,notnull=True,ddl="integer")
    name = StringField(notnull=True,ddl="varchar(100)",vrange="1-100")
    url = UrlField(ddl="varchar(4096)")
    info = StringField(ddl="varchar(1024)",vrange="0-1024")
    type = IntegerField(ddl="integer",vrange="1-100")
    level = IntegerField(ddl="integer",vrange="1-4")
    description = TextField(ddl="text")
    host_id = IntegerField(notnull=True,ddl="integer")


    def __eq__(self, other):
        if not isinstance(other,Vul):
            raise ModelError("the right instance is not Vul")

        return self.getVal('name') == other.getVal('name')


    @classmethod
    def create(cls):
        sqlCmd = ("create table if not exists vul ("
            "id integer primary key autoincrement,"
            "name varchar(100) not null,"
            "url varchar(4096),"
            "info varchar(1024),"
            "type integer,"
            "level integer,"
            "description text,"
            "host_id integer not null,"
            "unique (name, host_id) on conflict replace,"
            "foreign key (host_id) references host (id)"
            ")")
        cls.sqlexec(sqlCmd)


class Comment(Model):
    _table = "comment"

    id = IntegerField(primarykey=True,notnull=True,ddl="integer")
    name = StringField(notnull=True,ddl="varchar(100)",vrange="1-100")
    url = UrlField(ddl="varchar(4096)")
    info = StringField(ddl="varchar(1024)",vrange="0-1024")
    level = IntegerField(ddl="integer",vrange="1-4")
    attachment = StringField(ddl="varchar(200)",vrange="0-200")
    description = TextField(ddl="text")
    host_id = IntegerField(notnull=True,ddl="integer")


    def __eq__(self, other):
        if not isinstance(other,Comment):
            raise ModelError("the right instance is not Comment")

        return self.getVal('name') == other.getVal('name')


    @classmethod
    def create(cls):
        sqlCmd = ("create table if not exists comment ("
            "id integer primary key autoincrement, "
            "name varchar(100) not null,"
            "url varchar(4096),"
            "info varchar(1024),"
            "level integer,"
            "attachment varchar(200),"
            "description text,"
            "host_id integer not null,"
            "unique (name, host_id) on conflict replace,"
            "foreign key (host_id) references host (id)"
            ")")
        cls.sqlexec(sqlCmd)


class Database(Model):
    _tables = [Project, Host, Vul, Comment]

    @classmethod
    def create(cls):
        for table in cls._tables:
            table.create()

    @classmethod
    def delete(cls):
        dbFile = os.path.join("data", "database", CONF.db.name)
        if os.path.exists(dbFile):
            os.remove(dbFile)

    @classmethod
    def reset(cls):
        cls.delete()
        cls.create()


