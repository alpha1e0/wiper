#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os

import yaml

from plugin.lib.taskManager import PluginError


class SearchConfig(object):
	def __new__(cls, engine):
		configFile = os.path.join("plugin","config","searchengine.yaml")
		try:
			with open(configFile, "r") as fd:
				config = yaml.load(fd)[engine]
		except IOError:
			raise PluginError("open searchengine configure file 'plugin/config/searchengine.yaml' failed")
		else:
			return config


class Query(object):
	'''
	Build query string
	parameter:
		site: search in specified site
		title: search in title
		url: search in url
		filetype: search file with specified file type
		ext: search file with specified filet extention
		link: search in link
		kw: search keywords
	example:
		query(site="xxx.com") | -query(site="www.xxx.com")
	'''
	def __init__(self, **kwargs):
		self._qlist = list()
		for key,value in kwargs.iteritems():
			self._qlist.append(["",key,value])

	def __neg__(self):
		self._qlist[0][0] = "-"
		return self

	def __pos__(self):
		self._qlist[0][0] = "+"
		return self

	def __or__(self, obj):
		self._qlist += obj._qlist
		return self

	def genUrl(self, engine):
		config = SearchConfig(engine)
		for line in self._qlist:
			for item in line:


	def doSearch(engine="baidu", size=500, encode="utf-8"):
		url = self.genUrl(engine)



