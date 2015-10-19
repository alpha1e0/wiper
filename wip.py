#!/usr/bin/env python

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''


import init
from controller.application import startServer



if __name__ == "__main__":
	init.taskManager.run()
    startServer()
