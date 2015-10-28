#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import time
from multiprocessing import Process, queues, Queue

from config import CONF, WIPError
from model.orm import Model


class TaskError(WIPError):
	def __init__(self, reason):
		self.errMsg = "TaskError. " + ("reason: "+reason if reason else "")

	def __str__(self):
		return self.errMsg


class TaskManager(Process):
	'''
	Manage the task.
	Usage:
		task = TaskManager()
		plugin = ... #plugin see class 'Plugin'
		task.startTask(plugin)
	'''
	def __init__(self, timeout=2):
		Process.__init__(self)
		self.timeout = timeout

		#self._inQueue = Queue()
		#self._outQueue = Queue()


	def startTask(self, pluginObj, startData):
		'''
		Start task. send pluginObj to task process.
		input:
			pluginObj: the plugin object
			startData: the start data, a list of Model
		'''
		self._inQueue.put(pluginObj)
		# debug
		plugin = self._inQueue.get()
		print "get plugin", plugin.namestr

		for data in startData:
			self._outQueue.put(data)
		self._outQueue.put(Model())


	def run(self):
		print "debug: start taskManager"
		while True:
			try:
				print "debug: try to get plugin"
				pluginObj = self._inQueue.get(timeout=self.timeout)
				print "debug: ", "get plugin ", pluginObj
			except queues.Empty:
				continue
			else:
				pluginObj.startPlugin()


