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
import dns.exception

from init import log
from dbman.dbmanage import DBManage


class DnsOp:
	'''
	Dns operation
	'''
	def __init__(self, domain):
		self.domain = domain
		
		self.result = []

		self.resolver = dns.resolver.Resolver()
		self.resolver.nameservers = conf.dnsServers
		self.timeout = conf.dnsTimeout

		self.axfr = dns.query.axfr


	def getARecord(self):
		try:
			reponse = self.resolver.query(self.domain, "A")
		except dns.exception.DNSException:
			return False

		for line in reponse:
			self.result.append([self.domain, line.to_text(), "A"])

		return True


	def domain2IP(self, domain):
		domainToResolve = domain if domain else self.domain
		try:
			reponse = self.resolver.query(domainToResolve, "A")
		except dns.exception.DNSException:
			return False

		return response[0].to_text()


	def IP2domain(self, ip):
		return dns.reversename.from_address(ip)


	def getMXRecord(self):
		try:
			reponse = self.resolver.query(self.domain, "MX")
		except dns.exception.DNSException:
			return False

		for line in reponse:
			self.result.append([self.domain, line.to_text(), "MX"])

		return True


	def getNSRecord(self):
		try:
			reponse = self.resolver.query(self.domain, "NS")
		except dns.exception.DNSException:
			return False

		for line in reponse:
			self.result.append([self.domain, line.to_text(), "NS"])

		return True


	def getCNAMERecord(self):
		try:
			reponse = self.resolver.query(self.domain, "CNAME")
		except dns.exception.DNSException:
			return False

		for line in reponse:
			self.result.append([self.domain, line.to_text(), "CNAME"])

		return True


	def getSOARecord(self):
		try:
			reponse = self.resolver.query(self.domain, "SOA")
		except dns.exception.DNSException:
			return False

		for line in reponse:
			self.result.append([self.domain, line.to_text(), "SOA"])

		return True


	def getTXTRecord(self):
		try:
			reponse = self.resolver.query(self.domain, "TXT")
		except dns.exception.DNSException:
			return False

		for line in reponse:
			self.result.append([self.domain, line.to_text(), "TXT"])

		return True


	def getZoneRecord(self, server, pdomian):
		domain = pdomian if pdomian else self.domian
		xfr = self.axfr(server, domain)

		for reponse in xfr:
			for line in reponse.answer:
				if line.rdtype == 1:


	def resolveAll(self):
		pass


class ZoneTrans(multiprocessing.Process):
	'''
	Find and use DNS zone transfer vulnerability.
	'''
