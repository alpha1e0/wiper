#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import re

from plugin.lib.plugin import Plugin, PluginError
from plugin.lib.searchengine import Query
from model.model import Host

class GoogleHacking(Plugin):
	def __init__(self, size=200):
		super(GoogleHacking, self).__init__()
		self.size = size
		self.urlPattern = re.compile(r"^(?:http(?:s)?\://)?((?:[-0-9a-zA-Z_]+\.)+(?:[-0-9a-zA-Z_]+))")

	def handle(self, data):
		if not isinstance(data, Host):
			self.put(data)
		else:
			try:
				domain = data.url[4:] if data.url.startswith("www.") else data.url
			except AttributeError:
				raise PluginError("GoogleHacking plugin got an invalid model")
			query = Query(site=domain) | -Query(site="www."+domain)
			result = query.doSearch(engine="baidu", size=self.size)
			result += query.doSearch(engine="bing", size=self.size)

			urlSet = set()
			for i,key in enumerate(result):
				try:
					url = self.urlPattern.match(key[1]).groups()[0]
				except AttributeError:
					continue
				else:
					if url not in urlSet:
						urlSet.add(url)
						host = Host(title=key[0],url=url,description=key[2])
						self.put(host)
