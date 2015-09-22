#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import re

from modal.dbmanage import DBManage, escapeString
from init import log


class FieldError(Exception):
	def __init__(self, errorMsg):
		super(FieldError, self).__init__()
		self.value = errorMsg if errorMsg else "Field error!"

	def __str__(self):
		return self.value


class ModalError(Exception):
	def __init__(self, errorMsg):
		super(ModalError, self).__init__()
		self.value = errorMsg if errorMsg else "Modal error!"

	def __str__(self):
		return self.value


class Field(object):
	'''
	The base class of field.
	The filed attribute includes:
		name: the name of the Field 
		primarykey: True | False; the primarykey
		notnull: True | False; it means the 
		vrange: m-n; for string it means the length range, for integer it means the value range
		ddl: varchar(255)
		default: 
	'''
	def __init__(self, **kw):
		self.name = kw.get("name", None)
		self.primarykey = kw.get("primarykey", False)
		self.nullable = kw.get("notnull", False)
		self.default = kw.get("default", None)
		self.ddl = kw.get("ddl", None)

		vrange = kw.get("vrange", None)
		if vrange:
			try:
				vrange = (int(n) for n in vrange.split("-"))
			except ValueError:
				raise FieldError("AttrDefine Error, location {0}!".format(vrange))
			if vrange[0] > vrange[1]:
				raise FieldError("AttrDefine Error, location {0}!".format(vrange))

	def inputCheck(self, strValue):
		return True

	def inputFormat(self, strValue):
		'''
		The input data is a string, here format the input date to specified type.
			for example, the IntergetField().format("123") will format the string "123" to integer 123
		If failed, raise FieldError.
		'''
		return strValue


class IntegerField(Field):
	def __init__(self, **kw):
		super(IntegerField, self).__init__(**kw)

	def inputFormat(self, strValue):
		try:
			ret = int(strValue):
		except ValueError:
			raise FieldError("IntegerField Error, location:{0}, reason: integer value format error.".format(strValue,strValue))
		if self.vrange:
			if ret<self.vrange[0] or ret>self.vrange[1]:
				raise FieldError("IntegerField Error, location:{0}, reason: value out of range.".format(strValue))
			else:
				return ret
		else:
			return ret


class FloatField(Field):
	def __init__(self, **kw):
		super(FloatField, self).__init__(**kw)

class BooleanField(Field):
	def __init__(self, **kw):
		super(BooleanField, self).__init__(**kw)


class StringField(Field):
	def __init__(self, **kw):
		super(StringField, self).__init__(**kw)

	def inputFormat(self, strValue):
		if self.vrange:
			ret = escapeString(strValue)
			retLen = len(ret)
			if retLen<self.vrange[0] or retLen>self.vrange[1]:
				raise FieldError("StringField Error, location:{0}, reason: string length out of range.".format(strValue))
			else:
				return ret
		else:
			return ret


class TextField(Field):
	def __init__(self, **kw):
		super(TextField, self).__init__(**kw)


class UrlField(StringField):
	def __init__(self, **kw):
		super(UrlField, self).__init__(**kw)

	def inputFormat(self, strValue):
		if not strValue and isinstance(strValue,str):
			return strValue

		urlPattern = re.compile(r"^(?:http(?:s)?\://)?((?:[-0-9a-zA-Z_]+\.)+(?:[-0-9a-zA-Z_]+)(?:\:\d+)?)")
		match = urlPattern.match(strValue)
		if not match:
			raise FieldError("UrlField Error, location:{0}, reason: url format error.".format(strValue))
		else:
			return match.groups()[0]


class IPField(StringField):
	def __init__(self, **kw):
		super(IPField, self).__init__(**kw)

	def inputFormat(self, strValue):
		if not strValue and isinstance(strValue, str):
			return strValue

		ipPattern = re.compile(r"^((?:(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))\.){3}(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))(?:\:\d+)?)$")
		match = ipPattern.match(strValue)
		if not match:
			raise FieldError("IPField Error, location:{0}, reason: IP format error.".format(strValue))
		else:
			return match.groups()[0]


class EmailField(StringField):
	def __init__(self, **kw):
		super(EmailField, self).__init__(**kw)

	def inputFormat(self, strValue):
		if not strValue and isinstance(strValue, str):
			return strValue

		emailPattern = re.compile(r"^((?:[-0-9a-zA-Z_!=:.%+])+@(?:[-0-9a-zA-Z_!=:]+\.)+(?:[-0-9a-zA-Z_!=:]+))$")
		match = emailPattern.match(strValue)
		if not match:
			raise FieldError("EmailField Error, location:{0}, reason: Email format error.".format(strValue))
		else:
			return match.groups()[0]


class ModalMetaClass(type):
	'''
	The Metaclass will scan the attributes of the class and get some useful information.
	'''
	def __new__(cls, name, bases, attrs):
		if name == "Modal":
			return type.__new__(cls, name, bases, attrs)

		mapping = {}
		primaryKey = False
		for key,value in attrs.iteritems():		
			if isinstance(value, Field):
				if not value.name:
					value.name = key
				if value.primarykey:
					if not primaryKey:
						primaryKey = value
					else:
						raise ModalError("Model {0} Error, reason: Duplicate primary key.".format(name))
				mapping[key] = value

		if not primaryKey:
			raise ModelError("Model {0} Error, reason: Primary key not found.".format(name))

		attrs[__mapping] = mapping
		attrs[__primaryKey] = primaryKey

		return type.__new__(cls, name, bases, attrs)


class Model(dict):
	'''
	Base class for ORM.
	'''

	__metaclass__ = ModalMetaClass

	def __init__(self, **kw):
		self.where = ""
		super(Model, self).__init__(**kw)

