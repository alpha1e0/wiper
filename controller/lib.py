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
			#if type(value) == str:
			if isinstance(a, basestring):
				line[key] = stripSlashes(value)
	return qureryList

def queryResultToJson(queryResult):
	result = queryResultStripSlashes(queryResult)
	#result = [zip(nameList,line) for line in result]
	#result = [dict(line) for line in result]

	return json.dumps(result)


class ParamCheck(object):
	'''
	Description : Check param.
	Usage : ParamCheck(param, optinos)
	Parameters: 
		options: 
			descript the param
				((name,type,range),
			example:
				(("ip","ip",""),
			 	 ("url","url",""),
			 	 ("level","integer","1-5000"),
			 	 ("title","string","1-100"))
			type:
				ip, url, email, string, int, text
			range:
				if null, means everything
				integer: the number range
				string: the length range	
		param:
			the parameters
	'''
	def __init__(self,originParam,options):
		self.originParam = originParam
		self.options = options
		self.param = {}
		self.status = (True,"")

		self.ipPattern = re.compile(r"^((?:(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))\.){3}(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))(?:\:\d+)?)$")
		self.urlPattern = re.compile(r"^(?:http(?:s)?\://)?((?:[-0-9a-zA-Z_~!=]+\.)+(?:[-0-9a-zA-Z_~!=]+)(?:\:\d+)?)")
		self.emailPattern = re.compile(r"^((?:[-0-9a-zA-Z_!=:.%+])+@(?:[-0-9a-zA-Z_!=:]+\.)+(?:[-0-9a-zA-Z_!=:]+))$")


	def checkParam(self,option):
		if not self.status[0]:
			return False

		if option[1] == "ip":
			try:
				value = self.originParam[option[0]].strip()
			except KeyError:
				self.status = (False, "Missing parameter '{0}'!".format(option[0]))
				return False
			if not value and not option[2]:
				self.param[option[0]] = value
				self.status = (True, "")
			else:
				match = self.ipPattern.match(value)
				if not match:
					self.status = (False, "IP parameter '{0}' format error!".format(option[0]))
					return False
				self.param[option[0]] = match.groups()[0]
				self.status = (True, "")
		elif option[1] == "url":
			try:
				value = self.originParam[option[0]].strip()
			except KeyError:
				self.status = (False, "Missing parameter '{0}'!".format(option[0]))
				return False
			if not value and not option[2]:
				self.param[option[0]] = value
				self.status = (True, "")
			else:
				match = self.urlPattern.match(value)
				if not match:
					self.status = (False, "URL parameter '{0}' format error!".format(option[0]))
					return False
				self.param[option[0]] = match.groups()[0]
				self.status = (True, "")
		elif option[1] == "email":
			try:
				value = self.originParam[option[0]].strip()
			except KeyError:
				self.status = (False, "Missing parameter '{0}'!".format(option[0]))
				return False
			if not value and not option[2]:
				self.param[option[0]] = value
				self.status = (True, "")
			else:
				match = self.emailPattern.match(value)
				if not match:
					self.status = (False, "Email parameter '{0}' format error!".format(option[0]))
					return False
				self.param[option[0]] = match.groups()[0]
				self.status = (True, "")
		elif option[1] == "string":
			try:
				value = self.originParam[option[0]].strip()
			except KeyError:
				self.status = (False, "Missing parameter '{0}'!".format(option[0]))
				return False
			if option[2]:
				try:
					l,g=[int(x) for x in option[2].split("-")]
				except ValueError:
					self.status = (False, "Option string-range format error '{0}'!".format(option[2]))
					return False
				if len(value)>g or len(value)<l:
					self.status = (False, "String parameter '{0}' out of range!".format(option[0]))
					return False
				self.param[option[0]] = addSlashes(value)
				self.status = (True, "")
			else:
				self.param[option[0]] = addSlashes(value)
				self.status = (True, "")
		elif option[1] == "integer":
			try:
				value = int(self.originParam[option[0]].strip())
			except KeyError:
				self.status = (False, "Missing parameter '{0}'!".format(option[0]))
				return False
			except ValueError:
				if self.originParam[option[0]]:
					self.status = (False, "Integer parameter '{0}' format error!".format(option[0]))
					return False
				elif option[2]:
					self.status = (False, "Integer parameter '{0}' must not null!".format(option[0]))
					return False
				elif not option[2]:
					self.param[option[0]] = ""
					self.status = (True, "")
					return True
			if option[2]:
				try:
					l,g=[int(x) for x in option[2].split("-")]
				except ValueError:
					self.status = (False, "Option integer-range format error '{0}'!".format(option[2]))
					return False
				if l == g == 0:
					self.param[option[0]] = str(value)
					self.status = (True, "")
				elif value>g or value<1:
					self.status = (False, "Integer parameter '{0}' out of range!".format(option[0]))
					return False
				self.param[option[0]] = str(value)
				self.status = (True, "")
			else:
				self.param[option[0]] = str(value)
				self.status = (True, "")
		elif option[1] == "text":
			try:
				value = self.originParam[option[0]].strip()
			except KeyError:
				self.status = (False, "Missing parameter '{0}'!".format(option[0]))
				return False
			self.param[option[0]] = addSlashes(value)
			self.status = (True, "")
		else:
			self.status = (False, "Option type error, '{0}' is not recognized!".format(option[1]))
			return False

	def __enter__(self):
		for option in self.options:
			self.checkParam(option)

		return (self.status, type("Param", (), self.param))

	def __exit__(self, *unuse):
		pass





