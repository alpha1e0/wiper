#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import time
from multiprocessing import Process, Queue

from config import RTD


class PluginError(WIPError):
	def __init__(self, reason):
		self.errMsg = "PluginError. " + ("reason: "+reason if reason else "")

	def __str__(self):
		return self.errMsg


class Plugin(Process):
	'''
	The base class of plugin.
	Usage:
		class XXXPlugin(Plugin):
			def handle(self, data):
				result = doSomeThing(data)
				self.outQueue.put(result)
	Example: 
		plugin = (DNSTrans(timeout=5) + DomainBrute(dictlist) + GoogleHacking(engine='baidu')) | HttpRecognize() | DataSaver(mod="database") whill return a pluginObject
		
	'''
	def __init__(self, inQueue=None, outQueue=None):
		Process.__init__(self)

		self._inQueue = inQueue
		self._outQueue = outQueue
		if not self.inQueue:
			self.inQueue = RTD.taskManager.outQueue

		#addlist will record all the plugin object when use '+' or '|' operator
		self._addList = list()
		#orlist will record all the plugin object when use '+' operator
		self._orList = list()
		self.addAppend(self)
		self.orAppend(self)

		#indicate how many input-queue input data to self
		#when a process receive an empty object, it means the father process finish task and quit, 
		#if all the father processes quit, then self quit.
		self._inCounter = 1

		#record the new data from input queue, drop the duplicated data
		self._dataSet = set()


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


	def addAppend(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise TaskError("the object is not plugin")
		self._addList.append(pluginObj)

	def orAppend(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise TaskError("the object is not plugin")
		self._orList.append(pluginObj)


	def get(self, timeout=1):
		'''
		Get data from input queue.
		'''
		data = self.inQueue.get(timeout=timeout)
		if data in self._dataSet:
			raise Queue.Empty()
		else:
			self._dataSet.add(data)
			return data

	def put(self, data):
		'''
		Put data to output queue.
		'''
		self.outQueue.put(data)


	def __add__(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise TaskError("the right parameter is not plugin")

		for obj in pluginObj._addList:
			self.addAppend(obj)
		self.orAppend(pluginObj)

		return self


	def __or__(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise TaskError("the right parameter is not plugin")

		for obj in self._addList:
			pluginObj.addAppend(obj)

		queue = Queue()
		inLen = len(self._orList)
		for inObj in self._orList:
			for outObj in pluginObj._orList:
				outObj._inCounter = inLen
				inObj.outQueue = queue
				outObj.inQueue = queue

		return pluginObj


	def quit(self):
		'''
		Quit process. if the process finish a task, it sends an empty object.
		'''
		if self.outQueue:
			self.put(Model())


	def startPlugin(self):
		'''
		Start all plugins, this function will be called by TaskManager().startTask
		'''
		for plugin in self._addList:
			plugin.start()

	
	def run(self):
		'''
		Start process, the subclass must rewrite this function or 'handle' function
		when all the father processes quits, then break to quit
		'''
		counter = self._inCounter
		while True:
			try:
				data = self.get(timeout=1)
			except Queue.Empty:
				continue
			else:
				if data:
					self.handle(data)
				else:
					counter -= 1
					if not counter:
						self.quit()
						break


	def handle(self, data):
		'''
		Handle data, the subclass must rewrite this function or 'run' function
		'''
		pass

		