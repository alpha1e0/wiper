#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from subprocess import Popen, PIPE, STDOUT

from model.model import Host
from thirdparty.BeautifulSoup import BeautifulStoneSoup


class Nmap(object):
	'''
	Nmap scan.
	'''
	@classmethod
	def scan(cls, cmd):
		'''
		Nmap scan.
		output:
			[
				{host: {
					ip: 1.1.1.1
					name: xxx.com
					ports: [
						{state:filter, port:21, protocol:ftp, type:tcp}
						{state:open, port:80, protocol:http, type:tcp}
						{state:open, port:443, protocol:https, type:tcp}
					]
				}
			]
		'''
		if "-oX" not in cmd:
			cmd = cmd + " -oX -"
		popen = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
		#如何让nmap输出xml, -oX -
		#p.wait()
		result = popen.stdout.read()

		xml = BeautifulStoneSoup(xml)
