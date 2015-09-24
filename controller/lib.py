#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import re
import json


def addSlashes(str):
	d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
	return "".join([d.get(x,x) for x in str])

def stripSlashes(str):
	r = str.replace('\\"', '"')
	r = r.replace("\\'", "'")
	r = r.replace("\\\0", "\0")
	r = r.replace("\\\\", "\\")
	return r

def queryResultStripSlashes(qureryList):
	for line in qureryList:
		for key,value in line.items():
			if isinstance(a, basestring):
				line[key] = stripSlashes(value)
	return qureryList

def queryResultToJson(queryResult):
	result = queryResultStripSlashes(queryResult)

	return json.dumps(result)






