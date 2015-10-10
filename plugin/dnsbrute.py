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
from plugin.lib.dnsresolve import DnsResolver
from init import log


class DnsBrute(Plugin):
	'''
	Use wordlist to bruteforce subdomain.
	'''
	def __init__(self, domain, dictlist):
		super(DnsBrute, self).__init__(self)

		urlPattern = re.compile(r"^(?:http(?:s)?\://)?((?:[-0-9a-zA-Z_]+\.)+(?:[-0-9a-zA-Z_]+))")
		self.domain = urlPattern.match(domain.strip()).groups()[0]
		self.dictlist = [os.path.join("plugin","wordlist","dnsbrute",x) for x in dictlist]

		#partDoman示例：aaa.com partDomain为aaa，aaa.com.cn partDomain为aaa
		pos = self.domain.rfind(".com.cn")
		if pos==-1: pos = self.domain.rfind(".")
		self.partDomain = self.domain if pos==-1 else self.domain[0:pos]
		#去掉domain前面的www
		pos = self.domain.find("www.")
		self.domain = self.domain if pos==-1 else self.domain[pos+4:]

		dns = DnsResolver()
		#log.debug(self.dictlist+self.projectID+self.domain+self.partDomain)


	def checkDomain(self, domain):
#		try:
#			ip = socket.gethostbyname(domain)
#		except:
#			return False
#		return ip
		ips = dns.domain2IP(domain)
		if ips:
			return ips[0]


	def handle(self, data):
		if not isinstance(data, Host):
			self.put(data)
			return
		dlist = os.path.join("plugin","wordlist","toplevel.txt")
		for line in DictFileEnum(dlist):
			domain = self.partDomain + "." + line
			#log.debug(domain)
			ip = self.checkDomain(domain)
			if ip:
				self.put(Host(url=domain, ip=ip))

		for dlist in self.dictlist:
			for line in DictFileEnum(dlist):
				domain = line + "." + self.domain
				#log.debug(domain)
				ip = self.checkDomain(domain)
				if ip:
					self.put(Host(url=domain, ip=ip))



