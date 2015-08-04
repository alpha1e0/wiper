#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import web
import json
import sys

from dbman.dbmanage import DBManage
from init import log


def startServer():
	urls = (
		"/", "Index",
		"/addproject", "ProjectAdd",
		"/listproject", "ProjectList",
		"/getprojectdetail", "ProjectDetail",
		"/deleteproject", "ProjectDelete",
		"/modifyproject", "ProjectModify")

	app = web.application(urls, globals())

	app.run()


class Index:
	def GET(self):
		index = web.template.frender('server/index.html')

		return index()


class ProjectList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		sqlCmd = "select id,name from project order by 1"
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query project failed!')

		return json.dumps(dict(result))


class ProjectDetail:
	def GET(self):
		param = web.input()

		sqlCmd = "select name,url,ip,whois,ctime,description from project where id={0}".format(param.projectid.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror("Query project detail failed!")

		result = list(result[0])
		result[4] = result[4].strftime("%Y-%m-%d %H:%M:%S")

		return json.dumps(result)

class ProjectDelete:
	def GET(self):
		param = web.input()
		sqlCmd = "delete from project where id={0}".format(param.projectid.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror("Delete project failed!")

		return True


class ProjectModify:
	def POST(self):
		param = web.input()
		sqlCmd = "update project set name='{0}',url='{1}',ip='{2}',whois='{3}',description='{4}' where id={5}".format(\
			param.name.strip(), param.url.strip(), param.ip.strip(), param.whois.strip(), param.description.strip(), param.id.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Modify project failed!')
		
		return True


class ProjectAdd:
	def POST(self):
		param = web.input()
		sqlCmd = "insert into project(name, url, ip, whois, description) values('{0}', '{1}', '{2}', '{3}', '{4}')".format(\
			param.name.strip(), param.url.strip(), param.ip.strip(), param.whois.strip(), param.description.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Add project failed!')
		
		return True
