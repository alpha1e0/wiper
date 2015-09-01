#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

def addSlashes(str):
	d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
	return "".join([d.get(x,x) for x in str])

def stripSlashes(str):
	r = str.replace('\\"', '"')
	r = r.replace("\\'", "'")
	r = r.replace("\\\0", "\0")
	r = r.replace("\\\\", "\\")

	return r


class ParamCheck:
	'''
	Description : Check param.
	Usage : ParamCheck(param, optinos)
	Parameters: 
		options: 
			descript the param
				((name,type,range),(name,type,range))
			example:
				(("ip","t_ip",""),
			 	 ("url","t_url",""),
			 	 ("level","t_int","1-5000"),
			 	 ("title","t_string","1-100"))
			type:
				ip, url, email, string, int
			range:
				int: the number range
				string: the length range
				if null, means everything
		param:
			the parameters
	'''
	def __init__(self,originParam,options):
		self.originParam = originParam
		self.options = options
		self.param = {}
		self.param['errorMsg'] = ""

		ipPattern = re.compile(r"^((?:(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))\.){3}(?:(?:2[0-4]\d)|(?:255[0-5])|(?:[01]?\d\d?)))$")
		urlPattern = re.compile(r"^(?:http(s)?\://)?((?:[-0-9a-zA-Z_~!=:]+\.)+(?:[-0-9a-zA-Z_~!=:]+))", re.IGNORECASE)
		emailPattern = re.compile(r"^((?:[-0-9a-zA-Z_!=:.%+])+@(?:[-0-9a-zA-Z_!=:]+\.)+(?:[-0-9a-zA-Z_!=:]+))", re.IGNORECASE)


	def checkParam(self,option):
		if self.param['errorMsg']:
			return False

		if option[1] == "ip":
			try:
				value = self.originParam[option[0]]
			except KeyError:
				self.param['errorMsg'] = "Missing parameter {0}!".format(option[0])
				return False
			if not value and not option[2]:
				self.param[option[0]] = value
				self.param['errorMsg'] = ""
			else:
				match = ipPattern.match(value)
				if not match:
					self.errorMsg = "Parameter ip {0} formate error!".format(option[0])
					return False
				self.param[option[0]] = match.group()
				self.param['errorMsg'] = ""
		elif opton[1] == "url":
			try:
				value = self.originParam[option[0]]
			except KeyError:
				self.param['errorMsg'] = "Missing parameter {0}!".format(option[0])
				return False
			if not value and not option[2]:
				self.param[option[0]] = value
				self.param['errorMsg'] = ""
			else:
				match = urlPattern.match(value)
				if not match:
					self.errorMsg = "Parameter url {0} formate error!".format(option[0])
					return False
				self.param[option[0]] = match.groups()[1]
				self.param['errorMsg'] = ""
		elif opton[1] == "email":
			try:
				value = self.originParam[option[0]]
			except KeyError:
				self.param['errorMsg'] = "Missing parameter {0}!".format(option[0])
				return False
			if not value and not option[2]:
				self.param[option[0]] = value
				self.param['errorMsg'] = ""
			else:
				match = urlPattern.match(value)
				if not match:
					self.errorMsg = "Parameter email {0} formate error!".format(option[0])
					return False
				self.param[option[0]] = match.group()
				self.param['errorMsg'] = ""
		elif option[1] == "string":
			try:
				value = self.originParam[option[0]]
			except KeyError:
				self.param['errorMsg'] = "Missing parameter {0}!".format(option[0])
				return False
			if option[2]:
				try:
					l,g=[int(x) for x in "1-10".split("-")]
				except ValueError:
					self.param['errorMsg'] = "Option string range error {0}!".format(option[2])
					return False
				if len(value)>g or len(value)<l:
					self.param['errorMsg'] = "Parameter string {0} out of range!".format(option[0])
					return False
				self.param[option[0]] = libs.addSlashes(value)
				self.param['errorMsg'] = ""
			else:
				self.param[option[0]] = libs.addSlashes(value)
				self.param['errorMsg'] = ""
		elif option[1] == "int":
			try:
				value = int(self.originParam[option[0]])
			except KeyError:
				self.param['errorMsg'] = "Missing parameter {0}!".format(option[0])
				return False
			except ValueError:
				self.param['errorMsg'] = "Parameter integer {0} formate error!".format(option[0])
				return False
			if option[2]:
				try:
					l,g=[int(x) for x in "1-10".split("-")]
				except ValueError:
					self.param['errorMsg'] = "Option string range error {0}!".format(option[2])
					return False
				if value>g or value<1:
					self.param['errorMsg'] = "Parameter integer {0} out of range!".format(option[0])
					return False
				self.param[option[0]] = str(value)
				self.param['errorMsg'] = ""
			else:
				self.param[option[0]] = str(value)
				self.param['errorMsg'] = ""
		else:
			self.param['errorMsg'] = "Option type error {0}!".format(option[1])
			return False

	def __enter__(self):
		for option in self.options:
			self.checkParam(option)

		return type("Param", (), self.param)





