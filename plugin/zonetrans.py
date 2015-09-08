#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import multiprocessing

import dns.resolver
import dns.reversename
import dns.query

from init import log
from dbman.dbmanage import DBManage


class DnsOp:
	'''
	Dns operation
	'''
	def __init__(self, domain):
		self.domain = domain
		self.a = []
		self.mx = []
		self.ns = []
		self.cname = []
		self.soa = ""
		self.text = ""

	def getARecord(self):
		pass

	def getMXRecord(self):
		pass

	def getNSRecord(self):
		pass

	def getCNAMERecord(self):
		pass

	def getSOARecord(self):
		pass

	def getTEXTRecord(self):
		pass

	def axfrQuery(self):
		pass

	def resolveAll(self):
		pass
		

class ZoneTrans(multiprocessing.Process):
	'''
	Find and use DNS zone transfer vulnerability.
	'''
