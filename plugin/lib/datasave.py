#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''


from dbman.dbmanage import DBManage

class DataSaver(object):
	'''
	Save scan result.
	'''

	def __init__(self, mod='default'):
		pass

	def saveHosts(self, hostList, projectID):
		sqlCmdP = "insert into host(title,url,ip,protocol,level,os,server_info,middleware,description,project_id) values('{0}','{1}'\
				,'{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')"
		with DBManage() as dbcon:
			for host in hostList:
				sqlCmd = sqlCmdP.format(host.title,host.url,host.ip,host.protocol,host.level,host.os,host.server_info,host.middleware,host.description,projectID)
				dbcon.sql(sqlCmd)

		return True