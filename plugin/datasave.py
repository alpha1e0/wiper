#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from config import RTD
from plugin.lib.plugin import Plugin
from model.model import Project, Host, Vul, Comment


class DataSave(Plugin):
	def __init__(self, projectid=None, hostid=None):
		super(DataSave, self).__init__(timeout=1)
		self.projectid = projectid
		self.hostid = hostid

	def handle(self, data):
		if isinstance(data, Host):
			data.project_id = self.projectid
			data.save()
		elif isinstance(data, Vul) or isinstance(data, Comment):
			data.host_id = self.hostid
			data.save()
		elif isinstance(data, Project):
			data.save()
			pass

		print data