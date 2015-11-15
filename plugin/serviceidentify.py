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
from thirdparty.BeautifulSoup import BeautifulSoup

from plugin.lib.plugin import Plugin, PluginError
from plugin.lib.nmapwrapper import Nmap
from model.model import Host
from config import CONF


class ServiceIdentify(Plugin):
	'''
	Service identify plugin.
	Input:
		log: whether to log
		ptype: plugin running type.
			0: default, recognize service with default portList
			1: do not scan port, just do http recognize
			2: scan nmap inner portList
			3: scan 1-65535 port
	'''
	def __init__(self,log=True,ptype=0):
		super(ServiceIdentify, self).__init__(log=log)

		try:
			with open(os.path.join("plugin","config","portmapping.yaml"), "r") as fd:
				self.portDict = yaml.load(fd)
		except IOError:
			raise PluginError("cannot load portmapping configure file 'portmapping.yaml'")
			
		if ptype == 1:
			self.cmd = ""
		elif ptype == 2:
			self.cmd = "nmap -n -Pn -oX - "
		elif ptype == 3:
			self.cmd = "nmap -n -Pn -p1-65535 -oX - "
		else:
			portList = [key for key in self.portDict]
			portStr = ",".join([str(x) for x in portList])
			self.cmd = "nmap -n -Pn -p{ports} -oX - ".format(ports=portStr)

		self.type = ptype
		#requests.packages.urllib3.disable_warnings()
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

			if self.cmd:
				nmapCmd = self.cmd + hostStr
				result = Nmap.scan(nmapCmd)
			else:
				result = [data]

			for host in result:
				try:
					host.title = host.protocol + "_service"
				except AttributeError:
					pass
				host.protocol = self.portDict[int(host.port)]['protocol']
				try:
					if host.protocol in ["http","https"]:
						host.url = data.url
						host.description = data.description
						host.title = data.title
					host.level = data.level
				except AttributeError:
					pass				
				if host.protocol == "http":
					self.HTTPIdentify(host)
				elif host.protocol == "https":
					self.HTTPIdentify(host, https=True)

				self.put(host)


	def getTitle(self, rawContent, text):
		charset = None
		charsetPos = rawContent[0:500].lower().find("charset")
		if charsetPos != -1:
			charsetSlice = rawContent[charsetPos:charsetPos+18]
			charsetList = {"utf-8":"utf-8","utf8":"utf-8","gbk":"gbk","gb2312":"gb2312"}
			for key,value in charsetList.iteritems():
				if key in charsetSlice:
					charset = value
					break
		if not charset:
			charset = "utf-8"

		try:
			decodedHtml = rawContent.decode(charset)
			match = self.titlePattern.search(decodedHtml)
		except:
			match = self.titlePattern.search(text)

		return match.groups()[0] if match else "title not found"


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
			port = 443 if https else 80

		method = "https://" if https else "http://"
		url = method + url.strip("/") + ":" + str(port)

		try:
			response = requests.get(url, verify=False, timeout=self.httpTimeout)
		except:
			return

		host.title = self.getTitle(response.content, response.text)
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
