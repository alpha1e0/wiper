#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import HTMLParse

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


def genUrlParam(key, value, **kwargs):
	if kwargs:
		return "&".join([k+"="+v for k,v in kwargs.iteritems()]) + "&"
	else:
		return key + "=" + str(value) + "&"


class Query(object):
	'''
	Build query keyword
	parameter:
		site: seach specified site
		title: search in title
		url: search in url
		filetype: search files with specified file type
		ext: search files with specified extetion
		link: search in link
		kw: raw keywords to search 
	example:
		query = Query(site="xxx.com") | -Query(site="www.xxx.com") | Query(kw="password")
		query.doSearch(engine="baidu")
	'''
	def __init__(self, **kwargs):
		self._qlist = list()
		self.queryResult = list()

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


	def genKeyword(self, engine):
		'''
		Generate keyword string.
		'''
		config = SearchConfig("baidu")
		keyword = ""
		for line in self._qlsit:
			if line[1] in config['ghsyn']:
				line[1] = config['ghsyn'][line[1]]
				keyword += "".join(line)+" "
				continue
			elif line[1] == "kw":
				keyword += line[0]+line[2]

		return keyword


	def doSearch(engine="baidu", size=500, encode="utf-8"):
		keyword = self.genKeyword(engine)
		if engine == "baidu":
			baidu = Baidu(size=size, encode=encode)
			return baidu.search(keyword)
		else:
			return None


class Baidu(object):
	'''
	Baidu search engine.
	parameter:
		size: specified the amount of the result
		encode: specified the url encode method
	example:
		baidu=Baidu()
		baidu.search("site:xxx.com password.txt")
	'''
	def __init__(self, size=500, encode="utf-8"):
		self.size = size
		self.encode = encode

		self.config = SearchConfig("baidu")

		self.url = self.config['url']

		defaultParam = genUrlParam(None, None, **config['default'])
		self.url += defaultParam

		encodeParam = genUrlParam(self.config['param']['encode'], encode)
		self.url += encodeParam


	def search(self, keyword, size=None):
		size = size if size else self.size
		pageSize = self.config['param']['pgsize']['max']
		pages = size / pageSize

		keywordParam = genUrlParam(self.config['param']['query'], keyword)
		pageSizeParam = genUrlParam(self.config['param']['pgsize']['key'], keyword)

		url += keywordParam + pageSizeParam

		result = list()
		for p in xrange(pages+1):
			pageNumParam = genUrlParam(self.config['param']['pgnum'], p*pageSize)
			tmpurl = url + pageNumParam

			result.append(self._search(tmpurl))

		self.queryResult = result
		return result


	def _search(self, url):
		pass



