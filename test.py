#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import os
import random
import time
import urllib

import requests
import yaml
from thirdparty.BeautifulSoup import BeautifulSoup


class SearchConfig(object):
	def __new__(cls, engine):
		configFile = os.path.join("plugin","config","searchengine.yaml")
		try:
			with open(configFile, "r") as fd:
				config = yaml.load(fd)[engine]
		except IOError:
			print "read configfile error"
			return None
		else:
			return config


class UserAgents(object):
	def __new__(cls):
		configFile = os.path.join("plugin","config","useragent.yaml")
		try:
			with open(configFile, "r") as fd:
				config = yaml.load(fd)
		except IOError:
			userAgents = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
				"Mozilla/5.0 (Windows; U; Windows NT 5.2)Gecko/2008070208 Firefox/3.0.1",
				"Opera/9.27 (Windows NT 5.2; U; zh-cn)",
				"Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en)Opera 8.0)"]
		else:
			userAgents = [x['User-Agent'] for x in config]

		return userAgents


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
		for line in self._qlist:
			if line[1] in config['ghsyn']:
				keyword += line[0] + config['ghsyn'][line[1]] + ":" + line[2] + " "
			elif line[1] == "kw":
				keyword += line[0]+line[2] + " "

		return urllib.quote(keyword.strip())


	def doSearch(self, engine="baidu", size=500):
		'''
		Search in search engine.
		'''
		keyword = self.genKeyword(engine)
		if engine == "baidu":
			baidu = Baidu(size=size)
			return baidu.search(keyword)
		else:
			return None


class Baidu(object):
	'''
	Baidu search engine.
	parameter:
		size: specified the amount of the result
	example:
		baidu=Baidu()
		baidu.search("site:xxx.com password.txt")
	'''
	def __init__(self, size=500):
		self.size = size

		self.config = SearchConfig("baidu")
		self.userAgents = UserAgents()

		self.url = self.config['url']
		defaultParam = genUrlParam(None, None, **self.config['default'])
		self.url += defaultParam


	def search(self, keyword, size=None):
		'''
		Use baidu to search specified keyword.
		parameter:
			keyword: the keyword to search
			size: the length of search result
		'''
		size = size if size else self.size
		pageSize = self.config['param']['pgsize']['max']
		pages = size / pageSize

		keywordParam = genUrlParam(self.config['param']['query'], keyword)
		pageSizeParam = genUrlParam(self.config['param']['pgsize']['key'], pageSize)
		url = self.url + keywordParam + pageSizeParam

		result = list()
		for p in xrange(pages+1):
			pageNumParam = genUrlParam(self.config['param']['pgnum'], p*pageSize)
			tmpurl = url + pageNumParam

			result += self._search(tmpurl)

		self.queryResult = result
		return result


	def _search(self, url):
		'''
		Request with specified url, parse the reponse html document.
		parameter:
			url: the query url
		return:
			return the search result, result format is:
				[[titel,url,brief-information],[...]...]
		'''
		result = list()
		while True:
			#use timeout and random user-agent to bypass baidu IP restrict policy
			timeout = random.randint(1,3)
			time.sleep(timeout)

			userAgent = self.userAgents[random.randint(0,len(self.userAgents))-1]
			xforward = "192.168.3." + str(random.randint(1,255))
			headers = {"User-Agent":userAgent, "X-Forward-For":xforward}
			reponse = requests.get(url, headers=headers)
			# 判断是否返回了结果
			print url
			#print reponse.text
			print len(reponse.text)
			if len(reponse.text) > 1000:
				break

		document = BeautifulSoup(reponse.text)

		attrs={"class":"f"}
		relist = document.findAll("td", attrs=attrs)
		print relist[0]

		for line in relist:
			title = line.font.string
			url = line.a["href"]
			brief = line.a.nextSibling.nextSibling.contents[0]
			result.append([title, url, brief])

		print result
		return result




query = Query(site="huawei.com")
re = query.doSearch(size=5)
#print re

