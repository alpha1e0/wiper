#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import socket
import multiprocessing

from plugin.lib.tools import readList
from plugin.lib.tools import HostScanner
from init import log
from init import Enum
from dbman.dbmanage import DBManage

LEVEL = Enum(info=4,common=3,important=2,critical=1)

class DnsBrute(multiprocessing.Process):
	'''
	使用字典爆破子域名
	'''
	def __init__(self, url, projectID, dictlist):
		multiprocessing.Process.__init__(self)

		self.domain = url.strip()
		self.projectID = projectID
		self.dictlist = dictlist
		self.result = []
		#partDoman示例：aaa.com partDomain为aaa，aaa.com.cn partDomain为aaa
		pos = self.domain.rfind(".com.cn")
		if pos==-1: pos = self.domain.rfind(".")
		self.partDomain = self.domain if pos==-1 else self.domain[0:pos]
		#去掉domain前面的www
		pos = self.domain.find("www.")
		self.domain = self.domain if pos==-1 else self.domain[pos+4:]


	def checkDomain(self, domain):
		#这里使用python内置的gethostbyname来查询DNS记录
		try:
			ip = socket.gethostbyname(domain)
		except:
			return False
		return ip

	def bruteSubDomain(self):
		for dlist in self.dictlist:
			for line in readList(dlist):
				domain = line + "." + self.domain
				ip = self.checkDomain(domain)
				if ip:
					self.result.append([ip,domain,LEVEL.info])

	def bruteTopDomain(self):
		dlist = os.path.join("wordlist","toplevel.txt")
		for line in readList(dlist):
			domain = self.partDomain + "." + line
			ip = self.checkDomain(domain)
			if ip:
				self.result.append([ip,domain,LEVEL.info])

	def saveResult(self):
		dbcon = DBManage()

		sqlCmd = "insert into tmp_task_result_byhost(url,ip,level,source,project_id) values('{0}', '{1}', '{2}', '{3}', '{4}')"

		for i in self.result:
			sqlCmd.format(i[0],i[1],i[2],"dnsbrute",self.project_id)
			dbcon.sql(sqlCmd)

	def run(self):
		self.bruteTopDomain()
		self.bruteSubDomain()
		self.result = HostScanner.getHttpHosts(self.result)
		self.saveResult()



