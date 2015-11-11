#!/usr/bin/env python

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import multiprocessing

import config
from controller.application import startServer
from model.model import Project, Host, Vul, Comment


if __name__ == "__main__":
	config.RTD.taskManager = multiprocessing.Manager()

	startServer()
