#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import time
from multiprocessing import Process, managers, Lock

from config import RTD, WIPError, Log
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
    Input:
        timeout: the timeout of getting model data from queue
        unique: whether to drop the dumplicate model data
        log: whether to record log
    Usage:
        class XXXPlugin(Plugin):
            def handle(self, data):
                result = doSomeThing(data)
                self.outQueue.put(result)
    Example: 
        plugin = (DNSTrans(timeout=5) + DomainBrute(dictlist) + GoogleHackingPlugin(engine='baidu')) | HttpRecognize() | DataSavePlugin(mod="database") whill return a pluginObject
        plugin.dostart(startData)       
    '''

    def __init__(self, timeout=1, unique=True, log=True):
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

        self.log = True if log else False


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
            if self.log:
                self.log.info("plugin '{0}' got model {1}".format(self.__class__.__name__, data))
            return data


    def put(self, data):
        '''
        Put data to output queue.
        '''
        if self.log:
            self.log.info("plugin '{0}' put model {1}".format(self.__class__.__name__, data))

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
            time.sleep(0.5)
            plugin.start()

    
    def run(self):
        '''
        Start process, the subclass must rewrite this function or 'handle' function
        when all the father processes quits, then break to quit
        '''
        print "debug:", "plugin ", self.name, " start", "ins: ", self._ins, "outs: ", self._outs
        if self.log:
            self.log = Log("plugin")
            self.log.info("plugin {0} start, ins:{1}, outs:{2}".format(self.name, self._ins, self._outs))
        else:
            self.log = False

        while True:
            try:
                data = self.get()
                #print "debug:", "plugin ", self.name, "getting", "ins<<<<<<<<", [str(x) for x in self._ins]
            except QueueEmpty:
                continue
            except IOError:
                break
            except EOFError:
                break
            except PluginExit:
                self.quit()
                print "debug:", "plugin ", self.name, "quit"
                if self.log:
                    self.log.info("plugin {0} quit".format(self.name))
                break
            else:
                print "debug:", "plugin ", self.name, "got", data
                self.handle(data)
            finally:
                time.sleep(self.timeout)


    def handle(self, data):
        '''
        Handle data, the subclass must rewrite this function or 'run' function
        '''
        pass

        