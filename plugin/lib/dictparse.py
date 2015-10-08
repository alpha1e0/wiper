#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os


def DictFileEnum(fileName):
	if os.path.exists(fileName):
		with open(fileName, "r") as fd:
			for line in fd:
				if line and not line.startswith("#"):
					yield line.strip()



