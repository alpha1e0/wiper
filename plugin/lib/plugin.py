#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import time
from multiprocessing import Process, managers

from config import RTD, WIPError
from model.model import Model


class PluginError(WIPError):
	def __init__(self, reason):
		self.errMsg = "PluginError. " + ("reason: "+reason if reason else "")

	def __str__(self):
		return self.errMsg

class QueueEmpty(Exception):
	pass

class PluginExit(Exception):
	pass


class Plugin(Process):
	'''
	The base class of plugin.
	Usage:
		class XXXPlugin(Plugin):
			def handle(self, data):
				result = doSomeThing(data)
				self.outQueue.put(result)
	Example: 
		plugin = (DNSTrans(timeout=5) + DomainBrute(dictlist) + GoogleHacking(engine='baidu')) | HttpRecognize() | DataSave(mod="database") whill return a pluginObject
		plugin.dostart(startData)		
	'''
	def __init__(self, timeout=2, unique=True):
		Process.__init__(self)

		self.timeout = timeout
		self.unique = unique
		self._ins = list()
		self._outs = list()

		#addlist will record all the plugin object when use '+' or '|' operator
		self._addList = list()
		#orlist will record all the plugin object when use '+' operator
		self._orList = list()
		self.addAppend(self)
		self.orAppend(self)

		self._dataSet = list()


	def addAppend(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise PluginError("the right object is not plugin")
		self._addList.append(pluginObj)

	def orAppend(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise PluginError("the right object is not plugin")
		self._orList.append(pluginObj)


	def __add__(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise PluginError("the right parameter is not plugin")

		for obj in pluginObj._addList:
			self.addAppend(obj)
		self.orAppend(pluginObj)

		return self


	def __or__(self, pluginObj):
		if not isinstance(pluginObj, Plugin):
			raise PluginError("the right parameter is not plugin")

		for obj in self._addList:
			pluginObj.addAppend(obj)

		inLen = len(self._orList)
		for inObj in self._orList:
			for outObj in pluginObj._orList:
				queue = RTD.taskManager.list()
				inObj._outs.append(queue)
				outObj._ins.append(queue)
		return pluginObj


	def __contains__(self, obj):
		for data in self._dataSet:
			if data == obj:
				return True
		return False


	def get(self):
		'''
		Get data from input queues.
		'''
		if not self._ins:
			raise PluginExit()

		gotData = False
		for i,queue in enumerate(self._ins):
			try:
				data = queue.pop()
			except IndexError:
				continue
			else:
				if not data:
					del self._ins[i]
					continue
				else:
					if self.unique:
						if data in self:
							continue
						else:
							gotData = True
							self._dataSet.append(data)
							break
					else:
						gotData = True
						break

		if not gotData:
			raise QueueEmpty()
		else:
			return data


	def put(self, data):
		'''
		Put data to output queue.
		'''
		for queue in self._outs:
			queue.insert(0,data)


	def quit(self):
		'''
		Quit process. if the process finish a task, it sends an empty object.
		'''
		if self._outs:
			self.put(Model())


	def dostart(self, startData):
		'''
		Start plugins.
		'''
		for obj in self._addList:
			if not obj._ins:
				queue = RTD.taskManager.list()
				for data in startData:
					queue.insert(0,data)
				queue.insert(0,Model())
				obj._ins.append(queue)

		for plugin in self._addList:
			plugin.start()

	
	def run(self):
		'''
		Start process, the subclass must rewrite this function or 'handle' function
		when all the father processes quits, then break to quit
		'''
		print "debug:", "plugin ", self.name, " start", "ins: ", [str(x) for x in self._ins], "outs: ", [str(x) for x in self._outs]

		while True:
			try:
				data = self.get()
				print "debug:", "plugin ", self.name, "getting", data
			except QueueEmpty:
				continue
			except IOError:
				print "debug:", "plugin ", self.name, " IOError"
				break
			except EOFError:
				print "debug:", "plugin ", self.name, " EOFError"
				break
			except PluginExit:
				print "debug:", "plugin ", self.name, " doexit"
				self.quit()
				break
			else:
				self.handle(data)
			finally:
				time.sleep(self.timeout)
		print "debug:", self.name, "quit"


	def handle(self, data):
		'''
		Handle data, the subclass must rewrite this function or 'run' function
		'''
		pass

		