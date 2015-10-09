#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import socket
import multiprocessing
import re

from plugin.lib.dictparse import DictFileEnum
from plugin.lib.taskmanager import Plugin
from init import log


class DnsBrute():
	def __init__(self, domain, dictlist):
		super(DnsBrute, self).__init__(self)
		self.domain = domain
		self.dictlist = dictlist

	def dataHandle(self, data):
		bruter = Bruter(self.url, self.dictlist)

		result = bruter.brute()
		for line in result:
			self.put(Host(url=line[0], ip=line[1]))


class Bruter(object):
	'''
	Use wordlist to bruteforce subdomain.
	'''
	def __init__(self, url, dictlist):
		multiprocessing.Process.__init__(self)
		#log.debug("init here")
		urlPattern = re.compile(r"^(?:http(?:s)?\://)?((?:[-0-9a-zA-Z_~!=:]+\.)+(?:[-0-9a-zA-Z_~!=:]+))")
		self.domain = urlPattern.match(url.strip()).groups()[0]
		self.dictlist = [os.path.join("plugin","wordlist","dnsbrute",f) for f in dictlist]
		self.result = []
		#partDoman示例：aaa.com partDomain为aaa，aaa.com.cn partDomain为aaa
		pos = self.domain.rfind(".com.cn")
		if pos==-1: pos = self.domain.rfind(".")
		self.partDomain = self.domain if pos==-1 else self.domain[0:pos]
		#去掉domain前面的www
		pos = self.domain.find("www.")
		self.domain = self.domain if pos==-1 else self.domain[pos+4:]

		#log.debug(self.dictlist+self.projectID+self.domain+self.partDomain)


	def checkDomain(self, domain):
		#这里使用python内置的gethostbyname来查询DNS记录
		try:
			ip = socket.gethostbyname(domain)
		except:
			return False
		return ip


	def bruteSubDomain(self):
		for dlist in self.dictlist:
			for line in DictFileEnum(dlist):
				domain = line + "." + self.domain
				log.debug(domain)
				ip = self.checkDomain(domain)
				if ip:
					self.result.append([domain,ip])


	def bruteTopDomain(self):
		dlist = os.path.join("plugin","wordlist","toplevel.txt")
		for line in DictFileEnum(dlist):
			domain = self.partDomain + "." + line
			log.debug(domain)
			ip = self.checkDomain(domain)
			if ip:
				self.result.append([domain,ip])


	def brute(self):
		self.bruteTopDomain()
		self.bruteSubDomain()

		return self.result



