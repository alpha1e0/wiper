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
#import datetime.datetime

from dbman.dbmanage import DBManage
from init import log


dbcon = DBManage()


def startServer():
	urls = (
		"/", "Index",
		"/addproject", "ProjectAdd",
		"/listproject", "ProjectList")

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

		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query project failed!')

		#print result[0][5].strftime("%Y-%m-%d %H:%M:%S")
		return json.dumps(dict(result))


class ProjectAdd:
	def POST(self):
		data = web.input()
		sqlCmd = "insert into project(name, url, ip, whois, description) values('{0}', '{1}', '{2}', '{3}', '{4}')".format(\
			data.name.strip(), data.url.strip(), data.ip.strip(), data.whois.strip(), data.description.strip())

		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Add project failed!')
		
		return True
