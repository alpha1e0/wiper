#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os

from init import Enum

LEVEL = Enum(info=4,common=3,important=2,critical=1)

def readList(fileName):
	if os.path.exists(fileName):
		with open(fileName, "r") as fd:
			for line in fd:
				if line[0]!="#" and line!="":
					yield line.strip()


class HostScanner:
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