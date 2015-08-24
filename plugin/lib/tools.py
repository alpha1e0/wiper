#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os

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

	def hostScan(self):
		pass

	def portScan(self):
		pass

	def httpScan(self):
		pass