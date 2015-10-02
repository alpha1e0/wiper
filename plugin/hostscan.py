#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''



class HostScan(object):
	'''
	Scanner module, include hostscan, portscan, httpscan
	'''
	@staticmethod
	def hostScan():
		pass

	@staticmethod
	def portScan():
		pass

	@staticmethod
	def httpScan():
		pass

	@staticmethod
	def getHttpHosts(hostList):
		return hostList