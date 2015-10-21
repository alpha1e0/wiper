#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import re
import json

import web

from config import WIPError, rtd
from model.dbmanage import DBError
from model.orm import FieldError, ModelError


class ParamError(WIPError):
	def __init__(self, reason=""):
		self.errMsg = "ParamError. " + ("reason: "+reason if reason else "")

	def __str__(self):
		return self.errMsg


def addSlashes(str):
	d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
	return "".join([d.get(x,x) for x in str])

def stripSlashes(str):
	r = str.replace('\\"', '"')
	r = r.replace("\\'", "'")
	r = r.replace("\\\0", "\0")
	r = r.replace("\\\\", "\\")
	return r


def jsonSuccess():
	return json.dumps({'success':1})

def jsonFail():
	return json.dumps({'success':0})


def handleException(func):
	def _wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except KeyError:
			raise web.internalerror("Missing parameter.")
		except AttributeError:
			raise web.internalerror("Missing parameter.")
		except FieldError as error:
			raise web.internalerror(error)
		except ModelError as error:
			raise web.internalerror("Internal ERROR!")
		except DBError as error:
			rtd.log.error(error)
			raise web.internalerror("Internal ERROR!")

	return _wrapper


def formatParam(originParam,options):
	'''
	Description : Check param.
	Usage : params = formatParam(originParam, options)
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
	ipPattern = re.compile(r"^((?:(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))\.){3}(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))(?:\:\d+)?)$")
	urlPattern = re.compile(r"^(?:http(?:s)?\://)?((?:[-0-9a-zA-Z_~!=]+\.)+(?:[-0-9a-zA-Z_~!=]+)(?:\:\d+)?)")
	emailPattern = re.compile(r"^((?:[-0-9a-zA-Z_!=:.%+])+@(?:[-0-9a-zA-Z_!=:]+\.)+(?:[-0-9a-zA-Z_!=:]+))$")
	params = dict()

	for option in options:
		if option[1] == "ip":
			try:
				value = originParam[option[0]].strip()
			except KeyError:
				raise ParamError("missing parameter '{0}'".format(option[0]))
			if not value and not option[2]:
				params[option[0]] = value
			else:
				match = ipPattern.match(value)
				if not match:
					raise ParamError("IP parameter '{0}' format error".format(option[0]))
				params[option[0]] = match.groups()[0]
		elif option[1] == "url":
			try:
				value = originParam[option[0]].strip()
			except KeyError:
				raise ParamError("missing parameter '{0}'".format(option[0]))
			if not value and not option[2]:
				params[option[0]] = value
			else:
				match = urlPattern.match(value)
				if not match:
					raise ParamError("URL parameter '{0}' format error!".format(option[0]))
				params[option[0]] = match.groups()[0]
		elif option[1] == "email":
			try:
				value = originParam[option[0]].strip()
			except KeyError:
				raise ParamError("missing parameter '{0}'".format(option[0]))
			if not value and not option[2]:
				params[option[0]] = value
			else:
				match = emailPattern.match(value)
				if not match:
					raise ParamError("Email parameter '{0}' format error!".format(option[0]))
				params[option[0]] = match.groups()[0]
		elif option[1] == "string":
			try:
				value = originParam[option[0]].strip()
			except KeyError:
				raise ParamError("missing parameter '{0}'".format(option[0]))
			if option[2]:
				try:
					l,g=[int(x) for x in option[2].split("-")]
				except ValueError:
					raise ParamError("range option define error '{0}'!".format(option[2]))
				if len(value)>g or len(value)<l:
					raise ParamError("string parameter '{0}' out of range!".format(option[0]))
				params[option[0]] = addSlashes(value)
			else:
				params[option[0]] = addSlashes(value)
		elif option[1] == "integer":
			try:
				value = int(originParam[option[0]].strip())
			except KeyError:
				raise ParamError("missing parameter '{0}'".format(option[0]))
			except ValueError:
				if originParam[option[0]]:
					raise ParamError("integer parameter '{0}' format error!".format(option[0]))
				elif option[2]:
					raise ParamError("integer parameter '{0}' must not null!".format(option[0]))
				elif not option[2]:
					params[option[0]] = ""	
			if option[2]:
				try:
					l,g=[int(x) for x in option[2].split("-")]
				except ValueError:
					raise ParamError("range option define error '{0}'!".format(option[2]))
				if l == g == 0:
					params[option[0]] = str(value)
				elif value>g or value<1:
					raise ParamError("Integer parameter '{0}' out of range!".format(option[0]))
				params[option[0]] = str(value)
			else:
				params[option[0]] = str(value)
		elif option[1] == "text":
			try:
				value = originParam[option[0]].strip()
			except KeyError:
				raise ParamError("missing parameter '{0}'".format(option[0]))
			params[option[0]] = addSlashes(value)
		else:
			raise ParamError("option type '{0}' is not recognized!".format(option[1]))

	return type("Param", (), params)




