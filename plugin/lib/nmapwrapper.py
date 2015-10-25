#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from subprocess import Popen, PIPE, STDOUT

from model.model import Host
from thirdparty.BeautifulSoup import BeautifulStoneSoup, NavigableString


class Nmap(object):
	'''
	Nmap scan.
	'''
	@classmethod
	def scan(cls, cmd):
		'''
		Nmap scan.
		output:
			a list of Host
		'''
		result = list()

		if "-oX" not in cmd:
			cmd = cmd + " -oX -"
		popen = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
		scanResult = popen.stdout.read()

		#parse the nmap scan result		
		xmlDoc = BeautifulStoneSoup(scanResult)
		hosts = xmlDoc.findAll("host")
		for host in hosts:
			if isinstance(host, NavigableString) or host.name!="host" or host.status['state']!="up":
				continue
			ip = host.address['addr']
			#url = host.hostnames.hostname['name']
			try:
				ports = host.ports.contents
			except AttributeError:
				result.append(Host(**{'ip':ip}))
				continue
			else:
				findAlivePort = False
				for port in ports:
					if isinstance(port, NavigableString) or port.name != "port" or port.state['state']!="open": 
						continue
					findAlivePort = True
					hostDict = dict()
					hostDict['ip'] = ip
					hostDict['port'] = port['portid']
					hostDict['protocol'] = port.service['name']
					result.append(Host(**hostDict))
				if not findAlivePort:
					result.append(Host(**{'ip':ip}))

		return result
