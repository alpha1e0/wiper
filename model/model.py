#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from orm import Model, IntegerField, StringField, UrlField, IPField, TextField
from init import conf

class Project(Model):
	_table = "project"

	id = IntegerField(primarykey=True,notnull=True,ddl="integer")
	name = StringField(notnull=True,ddl="varchar(100)",vrange="1-100")
	url = UrlField(ddl="varchar(100)")
	ip = IPField(ddl="varchar(50)")
	level = IntegerField(notnul=True,ddl="integer",vrange="1-4")
	ctime = StringField(ddl="timestamp")
	whois = TextField(ddl="text")
	description = TextField(ddl="text")

	@classmethod
	def create(cls):
		sqlCmd = ("create table project ("
    		"id integer not null auto_increment,"
    		"name varchar(100) not null unique,"
    		"url varchar(100),"
    		"ip varchar(50),"
    		"level integer,"
    		"whois text,"
    		"ctime timestamp not null default CURRENT_TIMESTAMP,"
    		"description text,"
    		"primary key (id)"
			") engine=InnoDB  default charset=utf8;")
		cls.rawsql(sqlCmd)


class Host(Model):
	_table = "host"

	id = IntegerField(primarykey=True,notnull=True,ddl="integer")
	title = StringField(ddl="varchar(100)",vrange="0-100")
	url = UrlField(ddl="varchar(100)")
	ip = IPField(ddl="varchar(50)")
	protocol = IntegerField(notnull=True,ddl="integer",vrange="1-10")
	level = IntegerField(notnul=True,ddl="integer",vrange="1-4")
	os = StringField(ddl="varchar(150)",vrange="0-150")
	server_info = StringField(ddl="varchar(150)",vrange="0-150")
	middleware = StringField(ddl="varchar(200)",vrange="0-200")
	description = TextField(ddl="text")
	project_id = IntegerField(notnull=True,ddl="integer")

	@classmethod
	def create(cls):
		sqlCmd = ("create table host ("
		    "id integer not null auto_increment,"
		    "title varchar(200) not null,"
		    "url varchar(100),"
		    "ip varchar(50),"
		    "protocol integer not null,"
		    "level integer,"
		    "os varchar(150),"
		    "server_info varchar(150),"
		    "middleware varchar(200),"
		    "description text,"
		    "project_id integer not null,"
		    "unique key ipurl (ip, url),"
		    "primary key (id),"
		    "constraint project_id_host foreign key (project_id) references project (id)"
			") engine=InnoDB  default charset=utf8;")
		cls.rawsql(sqlCmd)


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

	@classmethod
	def create(cls):
		sqlCmd = ("create table vul ("
    		"id integer not null auto_increment,"
    		"name varchar(100),"
    		"url varchar(4096),"
    		"info varchar(1024),"
    		"type integer,"
    		"level integer,"
    		"description text,"
    		"host_id integer not null,"
    		"primary key (id),"
    		"constraint host_id_vul foreign key (host_id) references host (id)"
			") engine=InnoDB  default charset=utf8;")
		cls.rawsql(sqlCmd)


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

	@classmethod
	def create(cls):
		sqlCmd = ("create table comment ("
    		"id integer not null auto_increment, "
    		"name varchar(100), "
    		"url varchar(4096),"
    		"info varchar(1024), "
    		"level integer, "
    		"attachment varchar(200),"
    		"description text, "
    		"host_id integer not null, "
    		"primary key (id),"
    		"constraint host_id_comment foreign key (host_id) references host (id)"
			") engine=InnoDB  default charset=utf8;")
		cls.rawsql(sqlCmd)


class Database(Model):
	_tables = [Project, Host, Vul, Comment]

	@classmethod
	def create(cls):
		cls.rawsql("drop database if exists {0}".format(conf.dbname), raw=True)
		cls.rawsql("create database {0}".format(conf.dbname), raw=True)
		for table in cls._tables:
			table.create()

	@classmethod
	def reset(cls):
		cls.rawsql("drop database if exists {0}".format(conf.dbname), raw=True)
		cls.rawsql("create database {0}".format(conf.dbname), raw=True)
		for table in cls._tables:
			table.create()

