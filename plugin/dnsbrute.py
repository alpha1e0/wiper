#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import socket
import multiprocessing

from plugin.lib.tools import readList
from dbman.dbmanage import DBManage

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
		try:
			urlip = socket.gethostbyname(domain)
		except:
			return False
		return urlip

	def bruteSubDomain(self, dict):
		for line in readList(dict):
			domain = line + "." + self.domain
			urlip = self.checkDomain(domain)
			if urlip:
				self.result.append(urlip)

	def bruteTopDomain(self, dict):
		for line in readList(dict):
			domain = self.partDomain + "." + line
			urlip = self.checkDomain(domain)
			if urlip:
				self.result.append(urlip)

	#def record
