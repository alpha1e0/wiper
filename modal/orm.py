#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from modal.dbmanage import DBManage
from init import log

class FieldError(Exception):
	def __init__(self, errorMsg):
		super(FieldError, self).__init__()
		self.value = errorMsg if isinstance(errorMsg,str) else "Field error!"

	def __str__(self):
		return self.value


class Field(object):
	'''
	The base class of field.
	The filed attribute includes:
		primary_key: True | False
		notnull: True | False
		value_range: m-n
		ddl: varchar(255)
		default: 
	'''
	def __init__(self, **kw):
		self.primary_key = kw.get("primary_key", False)
		self.nullable = kw.get("notnull", False)
		self.default = kw.get("default", None)
		self.ddl = kw.get("ddl", None)

		value_range = kw.get("value_range", None)
		if value_range:
			value_range = (int(n) for n in value_range.split("-"))
			if value_range[0] > value_range[1]:
				raise FieldError("Value range error!")

	def check(self, value):
		pass

	def escape(self, value):
		return value



class IntegerField(Field):
	pass
