#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import multiprocessing

from init import log
from dbman.dbmanage import DBManage


class ZoneTrans(multiprocessing.Process):
	'''
	Find and use DNS zone transfer vulnerability.
	'''
