#!/usr/bin/env python

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''


import config
from controller.application import startServer
from plugin.lib.taskmanager import TaskManager



def init():
	config.RTD.log = config.Log()
	config.RTD.taskManager = TaskManager()


if __name__ == "__main__":
	init()

	config.RTD.taskManager.start()
    startServer()
