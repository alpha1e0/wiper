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


class query(object):
	'''
	Build query string
	parameter:
		size: indicate how much items of the search result
		site:
		title:
		url:
		filetype:
		ext:
		link:
		encode:
		kw:
	example:
		query(site="xxx.com") - query(site="www.xxx.com")
	'''
	def __init__(self, **kwargs):
		pass

	def __sub__(self, obj):
		pass

	def buildQueryString(self, engine="baidu"):
		pass


class Baidu(object):
	'''
	Simple baidu search engine client.
	parameter:
		size: indicate how much items of the search result
		site:
		title:
		url:
		filetype:
		ext:
		link:
		encode:
		kw:
	'''
	def __init__(self, **kwargs):