#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from subprocess import Popen, PIPE, STDOUT

class Nmap(object):
	def __init__(self, cmd):
		self.cmd = cmd.strip()
		if not self.cmd.startswith("nmap"):
			self.cmd = "nmap " + self.cmd

	def run(self):
		p = Popen('ls', shell=True, stdout=PIPE, stderr=STDOUT)
		#如何让nmap输出xml, -oX -
		#p.wait()
		self.result = p.stdout.read()