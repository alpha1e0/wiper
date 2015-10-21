#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import time
from multiprocessing import Process, Queue

from config import conf, WIPError
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
	def __init__(self):
		Process.__init__(self)

		self._inQueue = Queue()
		self._outQueue = Queue()


	def startTask(self, pluginObj, startData):
		'''
		Start task. send pluginObj to task process.
		input:
			pluginObj: the plugin object
			startData: the start data, a list of Model
		'''
		self.inQueue.put(pluginObj)

		for data in startData:
			self.outQueue.put(data)
		self.outQueue.put(Model())


	@property
	def inQueue(self):
	    return self._inQueue

	@property
	def outQueue(self):
	    return self._outQueue

	def run(self, pluginObj):
		while True:
			try:
				pluginObj = self._inQueue.get(timeout=2)
			except Queue.Empty:
				continue
			else:
				pluginObj.startPlugin()


