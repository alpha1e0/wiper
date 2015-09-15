#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os

import dns.resolver
import dns.reversename
import dns.query
import dns.exception

from init import conf



class DnsResolver(object):
	'''
	Dns operation.
	The records format is [domain, value, type]
	'''
	def __init__(self, domain):
		self.domain = domain
		
		self.records = []

		self.resolver = dns.resolver.Resolver()
		self.resolver.nameservers = conf.dnsServers
		self.resolver.timeout = conf.dnsTimeout
		#self.resolver.nameservers = ["223.5.5.5", "8.8.4.4"]
		#self.resolver.timeout = 3

		self.axfr = dns.query.xfr


	def domain2IP(self, domain=None):
		domainToResolve = domain if domain else self.domain
		try:
			reponse = self.resolver.query(domainToResolve, "A")
		except dns.exception.DNSException:
			return []

		return response[0].to_text()


	def IP2domain(self, ip):
		return dns.reversename.from_address(ip)


	def getRecords(self, rtype, domain=None):
		'''
		Get dns records, records type supports "A", "CNAME", "NS", "MX", "SOA", "TXT"
		'''
		if not rtype in ["A", "CNAME", "NS", "MX", "SOA", "TXT", "a", "cname", "ns", "mx", "soa", "txt"]:
			return []

		domainToResolve = domain if domain else self.domain
		try:
			reponse = self.resolver.query(domainToResolve, rtype)
		except dns.exception.DNSException:
			return []

		if rtype in ["MX","mx"]:
			return [[domainToResolve, line.to_text().rstrip(".").split()[-1], rtype] for line in reponse]
		return [[domainToResolve, line.to_text().rstrip("."), rtype] for line in reponse]


	def getZoneRecords(self, domain=None):
		domainToResolve = domain if domain else self.domain

		records = []
		nsRecords = self.getRecords("NS", domainToResolve)
		for serverRecord in nsRecords:
			xfrHandler = self.axfr(serverRecord[1], domainToResolve)
			try:
				for reponse in xfrHandler:
					topDomain = reponse.origin.to_text().rstrip(".")
					for line in reponse.answer:
						# A records
						if line.rdtype == 1:
							lineSplited = line.to_text().split()
							if lineSplited[0] != "@":
								subDomain = lineSplited[0] + "." + topDomain
								ip = lineSplited[-1]
								records.append([subDomain, ip, "A"])
						# CNAME records
						elif line.rdtype == 5:
							lineSplited = line.to_text().split()
							if lineSplited[0] != "@":
								subDomain = lineSplited[0] + "." + topDomain
								aliasName = lineSplited[-1]
								records.append([subDomain, aliasName, "CNAME"])
			except:
				pass

		return records


	def getZoneRecords2(self, server, domain=None):
		domainToResolve = domain if domain else self.domain

		records = []

		xfrHandler = self.axfr(server, domainToResolve)

		try:
			for reponse in xfrHandler:
				topDomain = reponse.origin.to_text().rstrip(".")
				for line in reponse.answer:
					# A records
					if line.rdtype == 1:
						lineSplited = line.to_text().split()
						if lineSplited[0] != "@":
							subDomain = lineSplited[0] + "." + topDomain
							ip = lineSplited[-1]
							records.append([subDomain, ip, "A"])
					# CNAME records
					elif line.rdtype == 5:
						lineSplited = line.to_text().split()
						subDomain = lineSplited[0] + "." + topDomain
						if lineSplited[0] != "@":
							aliasName = lineSplited[-1]
							records.append([subDomain, aliasName, "CNAME"])
		except:
			pass

		return records


	def resolveAll(self):
		types = ["A", "CNAME", "NS", "MX", "SOA", "TXT"]

		for t in types:
			self.records += self.getRecords(t)

		self.records += self.getZoneRecords()

		return self.records


