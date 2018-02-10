#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import time
import multiprocessing

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


class Plugin(multiprocessing.Process):
    '''
    The base class of plugin.
    Input:
        timeout: the timeout of getting model data from queue
        unique: whether to drop the dumplicate model data
        log: whether to record log
        stop: exit when receive stopcount empty data
    Usage:
        class XXXPlugin(Plugin):
            def handle(self, data):
                result = doSomeThing(data)
                self.outQueue.put(result)
    Example: 
        plugin = (DNSTrans(timeout=5) + DomainBrute(dictlist) + GoogleHackingPlugin(engine='baidu')) | HttpRecognize() | DataSavePlugin(mod="database") whill return a pluginObject
        plugin.dostart(startData)       
    '''

    STOP_LABEL = {"stop":"stop"}


    def __init__(self, inqueue, outqueue, timeout=2, unique=True, stopcount=1, 
        log=True):
        super(Plugin, self).__init__()

        self._inqueue = inqueue
        self._outqueue = outqueue

        self._timeout = timeout
        self._unique = unique

        self._stopCount = stopcount
        self._curStopCount = 0

        self._dataSet = list()

        self.log = True if log else None



    def __contains__(self, obj):
        for data in self._dataSet:
            if data == obj:
                return True
        return False


    def get(self):
        '''
        Get data from input queues.
        '''
        return self._inqueue.get()


    def put(self, data):
        '''
        Put data to output queue.
        '''
        self._outqueue.put(data)


    def is_stop(self, data):
        # stop when receive enough empty data, empty data {"stop":"stop"}
        if data == self.STOP_LABEL:
            self._curStopCount += 1
            if self._curStopCount >= self._stopCount:
                return True

        return False

    
    def run(self):
        '''
        Start process, the subclass must rewrite this function or 'handle' function
        when all the father processes quits, then break to quit
        '''

        if self.log:
            self.log = Log(self.name, toFile="plugin")
            self.log.info("plugin {0} start".format(
                self.name))
        else:
            self.log = False

        while True:
            try:
                data = self.get()
                #print "debug:", "plugin ", self.name, "getting", "ins<<<<<<<<", [str(x) for x in self._ins]
            except IOError:
                break
            except EOFError:
                break
            except PluginExit:
                break
            else:
                #print "debug:", "plugin ", self.name, "got", data
                self.handle(data)
            finally:
                time.sleep(self._timeout)


    def handle(self, data):
        '''
        Handle data, the subclass must rewrite this function or 'run' function
        '''
        if self.is_stop(data):
            raise PluginExit()

        if self._unique:
            if data in self._dataSet:
                return
            else:
                self._dataSet.add(data)

        self._handle(data)


    def _handle(self, data):
        raise NotImplementedError


        