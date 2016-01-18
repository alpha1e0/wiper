#!/usr/bin/env python

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import sys
import multiprocessing


if __name__ == "__main__":
    os.chdir(sys.path[0])

    import config
    config.RTD.taskManager = multiprocessing.Manager()
    
    from controller.application import startServer
    startServer()
