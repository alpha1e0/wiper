#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import time
from multiprocessing import Process, Queue

from init import conf, WIPError


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

	def startTask(self, pluginObj):
		# send pluginObj to task process with cmdQueue
		self._inQueue.put(pluginObj)

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


class Plugin(Process):
	'''
	The base class of plugin.
	Usage:
		class XXXPlugin(Plugin):
			def dataHandle(self, data):
				result = doSomeThing(data)
				self.outQueue.put(result)
	Example: 
		plugin = (DNSTrans(timeout=5) + DomainBrute() + GoogleHacking()) | HttpRecognize() | DataSaver(mod="database") whill return a pluginObject
		
	'''
	def __init__(self, inQueue, outQueue):
		Process.__init__(self)

		self._inQueue = inQueue
		self._outQueue = outQueue
		self._processList = list()

	@property
	def inQueue(self):
	    return self._inQueue
	
	@inQueue.setter
	def inQueue(self, queue):
		if not isinstance(queue, Queue):
			raise TaskError("the inQueue queue is not isinstance of Queue")
		self._inQueue = queue

	@property
	def outQueue(self):
	    return self._outQueue

	@outQueue.setter
	def outQueue(self, queue):
		if not isinstance(queue, Queue):
			raise TaskError("the outQueue queue is not isinstance of Queue")
		self._outQueue = queue


	def get(self, timeout=1):
		return self.inQueue.get(timeout=timeout)


	def put(self, data):
		self.outQueue.put(data)


	def __add__(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise TaskError("the right parameter is not plugin")

		if not self.inQueue:
			self.inQueue = conf.taskManager.outQueue

		if self not in self._processList:
			self._processList.append(self)
		if pluginObj not in self._processList:
			self._processList.append(pluginObj)


	def __or__(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise TaskError("the right parameter is not plugin")

		if not self.inQueue:
			self.inQueue = conf.taskManager.outQueue

		queue = Queue()
		self.outQueue = queue
		pluginObj.inQueue = queue

		if self not in self._processList:
			self._processList.append(self)
		if pluginObj not in self._processList:
			self._processList.append(pluginObj)


	def startPlugin(self):
		'''
		Start all plugins, this function will be called by TaskManager().startTask
		'''
		for plugin in self._processList:
			plugin.start()

	
	def run(self):
		'''
		Start process, the subclass must rewrite this function or 'dataHandle' function
		'''
		while True:
			try:
				data = self.get(timeout=1)
			except Queue.Empty:
				continue
			else:
				if data:
					self.dataHandle(data)
				else:
					break


	def dataHandle(self, data):
		'''
		Handle data, the subclass must rewrite this function or 'run' function
		'''
		pass
