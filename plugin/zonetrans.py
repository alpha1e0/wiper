#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import multiprocessing

from init import log
from plugin.lib.dnsresolve import DnsResolver


class ZoneTrans(multiprocessing.Process):
	'''
	Find and use DNS zone transfer vulnerability.
	'''

	def __init__(self, domain, projectID):
		multiprocessing.Process.__init__(self)

		self.domain = domain
		self.projectID = projectID

	def run(self):
		pass
