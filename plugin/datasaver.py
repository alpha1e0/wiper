#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from plugin.lib.taskmanager import TaskManager


class DataSaver(plugin):
	def __init__(self, projectid, hostid):
		super(self, DataSaver).__init__(self)
		self.projectid = projectid
		self.hostid = hostid

	def dataHandle(self, data):
		try:
			data.project_id = self.projectid
			data.host_id = self.hostid
		except AttributeError:
			pass
		finally:
			data.save()