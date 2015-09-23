#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import re
import json

from model.dbmanage import DBManage, escapeString
from init import log


class FieldError(Exception):
	def __init__(self, errorMsg):
		super(FieldError, self).__init__()
		self.value = errorMsg if errorMsg else "Field error!"

	def __str__(self):
		return self.value


class ModelError(Exception):
	def __init__(self, errorMsg):
		super(ModelError, self).__init__()
		self.value = errorMsg if errorMsg else "Model error!"

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
	def __init__(self, **kwargs):
		self.name = kwargs.get("name", None)
		self.primarykey = kwargs.get("primarykey", False)
		self.nullable = kwargs.get("notnull", False)
		self.default = kwargs.get("default", None)
		self.ddl = kwargs.get("ddl", None)

		vrange = kwargs.get("vrange", None)
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
	def __init__(self, **kwargs):
		super(IntegerField, self).__init__(**kwargs)

	def inputFormat(self, strValue):
		if not strValue and self.default:
			strValue = self.default
		if not strValue and self.notnull and not self.default:
			raise FieldError("IntegerField error, reason: the field must not null.".format(strValue,strValue))
		try:
			ret = int(strValue):
		except ValueError:
			raise FieldError("IntegerField error, location: {0}, reason: integer value format error.".format(strValue,strValue))
		if self.vrange:
			if ret<self.vrange[0] or ret>self.vrange[1]:
				raise FieldError("IntegerField error, location:{0}, reason: value out of range.".format(strValue))
			else:
				return ret
		else:
			return ret


class FloatField(Field):
	def __init__(self, **kwargs):
		super(FloatField, self).__init__(**kwargs)

class BooleanField(Field):
	def __init__(self, **kwargs):
		super(BooleanField, self).__init__(**kwargs)


class StringField(Field):
	def __init__(self, **kwargs):
		super(StringField, self).__init__(**kwargs)

	def inputFormat(self, strValue):
		if not strValue and self.default:
			strValue = self.default
		if not strValue and self.notnull:
			raise FieldError("StringField error, reason: the field must not null.".format(strValue,strValue))
		if self.vrange:
			ret = escapeString(strValue)
			retLen = len(ret)
			if retLen<self.vrange[0] or retLen>self.vrange[1]:
				raise FieldError("StringField error, location:{0}, reason: string length out of range.".format(strValue))
			else:
				return ret
		else:
			return ret


class TextField(Field):
	def __init__(self, **kwargs):
		super(TextField, self).__init__(**kwargs)


class UrlField(StringField):
	def __init__(self, **kwargs):
		super(UrlField, self).__init__(**kwargs)

	def inputFormat(self, strValue):
		if not strValue and self.default:
			strValue = self.default
		if not strValue and self.notnull:
			raise FieldError("UrlField error, reason: the field must not null.".format(strValue,strValue))

		urlPattern = re.compile(r"^(?:http(?:s)?\://)?((?:[-0-9a-zA-Z_]+\.)+(?:[-0-9a-zA-Z_]+)(?:\:\d+)?)")
		match = urlPattern.match(strValue)
		if not match:
			raise FieldError("UrlField error, location:{0}, reason: url format error.".format(strValue))
		else:
			return match.groups()[0]


class IPField(StringField):
	def __init__(self, **kwargs):
		super(IPField, self).__init__(**kwargs)

	def inputFormat(self, strValue):
		if not strValue and self.default:
			strValue = self.default
		if not strValue and self.notnull:
			raise FieldError("IPField error, reason: the field must not null.".format(strValue,strValue))

		ipPattern = re.compile(r"^((?:(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))\.){3}(?:(?:2[0-4]\d)|(?:25[0-5])|(?:[01]?\d\d?))(?:\:\d+)?)$")
		match = ipPattern.match(strValue)
		if not match:
			raise FieldError("IPField error, location:{0}, reason: IP format error.".format(strValue))
		else:
			return match.groups()[0]


class EmailField(StringField):
	def __init__(self, **kwargs):
		super(EmailField, self).__init__(**kwargs)

	def inputFormat(self, strValue):
		if not strValue and self.default:
			strValue = self.default
		if not strValue and self.notnull:
			raise FieldError("EmailField error, reason: the field must not null.".format(strValue,strValue))

		emailPattern = re.compile(r"^((?:[-0-9a-zA-Z_!=:.%+])+@(?:[-0-9a-zA-Z_!=:]+\.)+(?:[-0-9a-zA-Z_!=:]+))$")
		match = emailPattern.match(strValue)
		if not match:
			raise FieldError("EmailField error, location:{0}, reason: Email format error.".format(strValue))
		else:
			return match.groups()[0]


class ModelMetaClass(type):
	'''
	The Metaclass will scan the attributes of the class and get some useful information.
	'''
	def __new__(cls, name, bases, attrs):
		if name == "Model" or name == "Database":
			return type.__new__(cls, name, bases, attrs)

		if "__table" not in attrs:
			raise ModelError("Model {0} error, reason: attribute '__table' not specified.".format(name))

		mapping = dict()
		primaryKey = False
		notnulls = dict()
		for key,value in attrs.iteritems():		
			if isinstance(value, Field):
				if not value.name:
					value.name = key
				if value.primarykey:
					if not primaryKey:
						primaryKey = value
					else:
						raise ModelError("Model {0} error, reason: duplicate primary key.".format(name))
				mapping[key] = value

		if not primaryKey:
			raise ModelError("Model {0} error, reason: primary key not found.".format(name))

		attrs[__mapping] = mapping
		attrs[__primaryKey] = primaryKey

		return type.__new__(cls, name, bases, attrs)


class Model(dict):
	'''
	Base class for ORM.
	'''

	__metaclass__ = ModelMetaClass

	__orderby = ""
	__where = ""

	def __init__(self, **kwargs):
		super(Model, self).__init__(**kwargs)
		self.saveType = "insert"

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError("Model object has no attribute '{0}'".format(key))

	def __setattr__(self, key, value):
		self[key] = value


	@classmethod
	def rawsql(cls, sqlCmd):
		'''
		Execute sql command direct.
		'''
		with SQLExec(sqlCmd) as result:
			return result

	@classmethod
	def rawquery(cls, sqlCmd):
		'''
		Execute select query direct.
		'''
		with SQLQuery(sqlCmd) as result:
			return result

	@classmethod
	def create(cls):
		'''
		Create table.
		'''
		pass

	@classmethod
	def __clearStatus(cls):
		cls.__orderby = ""
		cls.__where = ""

	@classmethod
	def __paramFormat(cls, params):
		if not params:
			return False

		ret = dict()
		for key,value in params.iteritems():
			try:
				tmpValue = cls.__mapping[key].inputFormat(value)
			except KeyError:
				raise ModelError("Model error, location:{0}, reason: the model did not have key {1}.".format(cls.__class__.__name__, key))
			else:
				ret[key] = tmpValue

		return ret


	@classmethod
	def where(cls, **kwargs):
		'''
		Set the 'where' part of the SQL command. 
		'''
		if not kwargs:
			return cls
		params = cls.__paramFormat(kwargs)
		strList = ["{0}='{1}'".format(k,v) for k,v in params.iteritems()]
		cls.__where = "where " + " and ".join(strList)
		return cls

	@classmethod
	def orderby(cls, orderby=1):
		'''
		Set the 'order by' part of the SQL command. 
		'''
		cls.__orderby = "order by {0}".format(orderby)
		return cls


	@classmethod
	def findraw(cls, *args):
		'''
		Select from database, return the 'raw' data.
		Example: User.where(name='aa').findraw('name','ip','url')
			will returns: [{'name':'aa','ip','1.1.1.1','url':'test.com'},{'name':....}]
		'''
		if args:
			columns = ",".join(args)
		else:
			columns = "*"

		sqlCmd = "select {col} from {table} {where} {orderby}".format(col=columns,table=cls.__table,where=cls.__where,orderby=cls.__orderby)
		cls.__clearStatus()

		with SQLQuery(sqlCmd) as result:
			return result


	@classmethod
	def find(cls, *args):
		'''
		Select from database, return a list of model object
		Example: 
			User.where(name='aa').findraw('name','ip','url') will returns: [User(),User()]
			User.findraw() will return all the rows
		'''
		if args:
			columns = ",".join(args)
		else:
			columns = "*"

		sqlCmd = "select {col} from {table} {where} {orderby}".format(col=columns,table=cls.__table,where=cls.__where,orderby=cls.__orderby)
		cls.__clearStatus()

		with SQLQuery(sqlCmd) as result:
			ret = list()
			for line in result:
				obj = cls(**line)
				obj.saveType = "update"
				ret.append(obj)

		return ret


	@classmethod
	def getraw(cls, pvalue, *args):
		'''
		User primary key to select from database, return 'raw' data.
		'''
		if args:
			columns = ",".join(args)
		else:
			columns = "*"

		pvalue = cls.__primaryKey.inputFormat(pvalue)
		sqlCmd = "select * from {table} where {key}={value}".format(table=cls.__table,key=cls.__primaryKey.name,value=pvalue)

		with SQLQuery(sqlCmd) as result:
			return result[0]


	@classmethod
	def get(cls, pvalue, *args):
		'''
		User primary key to select from database, return a model object.
		'''
		if args:
			columns = ",".join(args)
		else:
			columns = "*"

		pvalue = cls.__primaryKey.inputFormat(pvalue)
		sqlCmd = "select * from {table} where {key}={value}".format(table=cls.__table,key=cls.__primaryKey.name,value=pvalue)

		with SQLQuery(sqlCmd) as result:
			if result:
				obj = cls(**result[0])
				obj.saveType = "update"
				return obj


	@classmethod
	def insert(cls, **kwargs):
		'''
		Insert a row to the database.
		Example: User.insert(name='aa',ip='1.1.1.1',url='test.com')
		'''
		if not kwargs:
			return False

		params = cls.__paramFormat(kwargs)
		keys = ",".join([k for k in params])
		values = ",".join(["'"+params[k]+"'" for k in params])

		salCmd = "insert into {table}({keys}) values({values})".format(table=cls.__table,keys=keys,values=values)
		with SQLExec(sqlCmd) as result:
			return result


	@classmethod
	def inserts(cls, rows):
		'''
		Insert some rows to the database.
		Param:
			rows: a list of dict which contains the data
		Example: User.inserts([{'name':'aa','ip','1.1.1.1','url':'test.com'},{'name':....}])
		'''
		if not rows:
			return False

		sqlCmdList = list()
		for row in rows:
			params = cls.__paramFormat(row)
			keys = ",".join([k for k in params])
			values = ",".join(["'"+params[k]+"'" for k in params])

			sqlCmdList.append("insert into {table}({keys}) values({values})".format(table=cls.__table,keys=keys,values=values))

		with DBManage() as con:
			for sqlCmd in sqlCmdList:
				con.sql(sqlCmd)


	@classmethod
	def update(cls, **kwargs):
		'''
		Update a row.
		Example: User.where(id=100).update(name='bb',ip='2.2.2.2')
		'''
		if not kwargs:
			return False

		params = cls.__paramFormat(kwargs)
		setValue = [k+"='"+v+"'" for k,v in params.iteritems]
		setValue = ",".join(setValue)

		sqlCmd = "update {table} set {setvalue} {where}".format(table=cls.__table,setvalue=setValue,where=cls.__where)
		cls.__clearStatus()
		with SQLExec(sqlCmd) as result:
			return result


	@classmethod
	def updates(cls, rows):
		pass


	@classmethod
	def delete(cls, pvalue=None):
		'''
		Delete rows from database.
		Example:
			User.delete(10) will delete row where primary key is 10
			User.where(name='aa').delete() while delete rows where name is 'aa'
		'''
		if pvalue:
			pvalue = cls.__primaryKey.inputFormat(pvalue)
			sqlCmd = "delect from {table} where {key}={value}".format(table=cls.__table,key=cls.__primaryKey.name,value=pvalue)
		else:
			sqlCmd = "delect from {table} {where}".format(table=cls.__table,where=cls.__where)
			__clearStatus()

		with SQLExec(sqlCmd) as result:
			return result


	@classmethod
	def deletes(cls, rows):
		pass

	def save(self):
		'''
		Save current object, will insert a row into database.
		Exaple:
			u=User(name='aa')
			u.save()

			u=User.get(10)
			u.name='bb'
			u.save()
		'''
		if self.saveType == "insert":
			params = self.__paramFormat(self)
			keys = ",".join([k for k in params])
			values = ",".join(["'"+params[k]+"'" for k in params])
			salCmd = "insert into {table}({keys}) values({values})".format(table=self.__table,keys=keys,values=values)
		elif self.saveType == "update":
			params = self.__paramFormat(self)
			setValue = [k+"='"+v+"'" for k,v in params.iteritems if k!=self.__primaryKey.name]
			setValue = ",".join(setValue)
			where = "where " + "{key}={value}".format(key=self.__primaryKey.name,value=self[self.__primaryKey.name])
			sqlCmd = "update {table} set {setvalue} {where}".format(table=self.__table,setvalue=setValue,where=where)

		with SQLExec(sqlCmd) as result:
			return result


	def remove(self):
		'''
		Remove current object, will delete a row from database.
		'''
		sqlCmd = "delect from {table} where {key}={value}".format(table=self.__table,key=self.__primaryKey.name,value=self[self.__primaryKey.name])

		with SQLExec(sqlCmd) as result:
			return result


	def toJson(self):
		return json.dumps(self)










