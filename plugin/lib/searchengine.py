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


def searchConfig(name):
	configFile = os.path.join("plugin","config","searchengine.yaml")
	try:
		with open(configFile, "r") as fd:
			config = yaml.load(fd)[name]
	except IOError:
		raise PluginError("open searchengine configure file 'plugin/config/searchengine.yaml' failed")
	else:
		return config


class Query(object):
	'''
	Build query string
	parameter:
		site:
		title:
		url:
		filetype:
		ext:
		link:
		kw:
	example:
		query(site="xxx.com") - query(site="www.xxx.com")
	'''
	def __init__(self, **kwargs):
		for key,value in kwargs.iteritems():
			self.kw = "{0}={1} ".format(key,value)

	def __sub__(self, obj):
		pass

	def __and__(self, obj):
		pass

	def __or__(self, obj):
		pass


	def doSearch(engine="baidu", size=500, encode="utf-8"):
		pass



