#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import re

from thirdparty import yaml
from thirdparty import requests

from plugin.lib.plugin import Plugin, PluginError
from plugin.lib.nmapwrapper import Nmap
from model.model import Host
from config import CONF


class ServiceIdentify(Plugin):
	def __init__(self,log=True):
		super(ServiceIdentify, self).__init__(log=log)

		try:
			with open(os.path.join("plugin","config","portmapping.yaml"), "r") as fd:
				self.portDict = yaml.load(fd)
		except IOError:
			raise PluginError("cannot load portmapping configure file 'portmapping.yaml'")

		self.portList = [key for key in self.portDict]

		requests.packages.urllib3.disable_warnings()
		self.httpTimeout = CONF.http.timeout
		self.titlePattern = re.compile(r"(?:<title>)(.*)(?:</title>)")


	def handle(self, data):
		if not isinstance(data, Host):
			self.put(data)
		else:
			try:
				hostStr = data.url
			except AttributeError:
				try:
					hostStr = data.ip
				except AttributeError:
					raise PluginError("ServiceIdentify plugin got an invalid model")
			portStr = ",".join([str(x) for x in self.portList])
			cmd = "nmap -n -Pn -p{ports} {host} -oX -".format(ports=portStr, host=hostStr)
			result = Nmap.scan(cmd)

			for host in result:
				try:
					host.url = data.url
					host.description = data.description
					host.title = data.title
					host.level = data.level
				except AttributeError:
					pass
				host.protocol = self.portDict[int(host.port)]['protocol']
				if host.protocol == "http":
					self.HTTPIdentify(host)
				elif host.protocol == "https":
					self.HTTPIdentify(host, https=True)

				self.put(host)


	def HTTPIdentify(self, host, https=False):
		try:
			url = host.url
		except AttributeError:
			try:
				url = host.ip
			except AttributeError:
				return
		try:
			port = host.port
		except AttributeError:
			if https:
				port = 443
			else:
				port = 80

		method = "https://" if https else "http://"

		url = method + url.strip("/") + ":" + str(port)

		try:
			response = requests.get(url, verify=False, timeout=self.httpTimeout)
		except:
			return

		try:
			host.title
		except AttributeError:
			match = self.titlePattern.search(response.text)
			if match:
				host.title = match.groups()[0]
			else:
				host.title = "title not found"

		try:
			server = response.headers['server']
		except (IndexError, KeyError):
			pass
		else:
			host.server_info = server

		try:
			middleware = response.headers['x-powered-by']
		except (IndexError, KeyError):
			pass
		else:
			host.middleware = middleware


	def FTPIdentify(self, host):
		pass
