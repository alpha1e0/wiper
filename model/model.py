#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from model.orm import Model
from init import conf

class Project(Model):
	__table = "project"

	id = IntergetField(primarykey=True,notnull=True,ddl="integer")
	name = StringField(notnull=True,ddl="varchar(100)",vrange="1-100")
	url = UrlField(ddl="varchar(100)")
	ip = IPField(ddl="varchar(50)")
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
    		"whois text,"
    		"ctime timestamp not null default CURRENT_TIMESTAMP,"
    		"description text,"
    		"primary key (id)"
			") engine=InnoDB  default charset=utf8;")
		cls.rawsql(sqlCmd)


class Host(Model):
	__table = "host"

	id = IntergetField(primarykey=True,notnull=True,ddl="integer")
	title = StringField(ddl="varchar(100)",vrange="0-100")
	url = UrlField(ddl="varchar(100)")
	ip = IPField(ddl="varchar(50)")
	protocol = IntegerField(notnull=True,ddl="integer",vrange="1-10")
	level = IntegerField(notnul=True,ddl="integer",vrange="1-4")
	os = StringField(ddl="varchar(150)",vrange="0-150")
	server_info = StringField(ddl="varchar(150)",vrange="0-150")
	middleware = StringField(ddl="varchar(200)",vrange="0-200")
	description = TextField(ddl="text")
	project_id IntegerField(notnull=True,ddl="integer")

	@classmethod
	def create(cls):
		sqlCmd = ("create table host ("
		    "id integer not null auto_increment,"
		    "title varchar(200) not null unique,"
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
	__table = "vul"

	id = IntergetField(primarykey=True,notnull=True,ddl="integer")
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
	__table = "comment"

	id = IntergetField(primarykey=True,notnull=True,ddl="integer")
	name = StringField(notnull=True,ddl="varchar(100)",vrange="1-100")
	url = UrlField(ddl="varchar(4096)")
	info = StringField(ddl="varchar(1024)",vrange="0-1024")
	level = IntegerField(ddl="integer",vrange="1-4")
	attachment = StringField(ddl="varchar(200)",vrange="1-200")
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


class Datebase(Model):
	__tables = [Project, Host, Vul, Comment]

	@classmethod
	def createDatabase(cls):
		cls.rawsql("drop database if exists {0}".format(conf.dbname))
		cls.rawsql("create database {0}".format(conf.dbname))
		for table in __tables:
			table.create()

	@classmethod
	def resetDatabase(cls):
		cls.rawsql("drop database if exists {0}".format(conf.dbname))
		cls.rawsql("create database {0}".format(conf.dbname))
		for table in __tables:
			table.create()
