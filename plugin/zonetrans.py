#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''


from plugin.lib.plugin import Plugin
from plugin.lib.dnsresolve import DnsResolver
from model.model import Host


class ZoneTrans(Plugin):
	'''
	Find and use DNS zone transfer vulnerability.
	'''

	def handle(self, data):
		if not isinstance(data, Host):
			self.put(data)
		else:
			dnsresolver = DnsResolver(data.url)
			records = dnsresolver.getZoneRecords()
			for line in records:
				if line[2] == "A":
					self.put(Host(url=line[0], ip=line[1]))
				elif line[2] == "CNAME":
					self.put(Host(url=line[0], description="alias "+line[1]))

