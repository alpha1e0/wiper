#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''


import sys
import os
import time
import json

import web

import lib
from model.orm import FieldError, ModelError
from model.model import Database, Project, Host, Vul, Comment
from model.dbmanage import DBError
from plugin.dnsbrute import DnsBrute
from init import log, conf, WIPError


def startServer():
	urls = (
		"/", "Index",
		"/install", "Install",
		"/addproject", "ProjectAdd",
		"/listproject", "ProjectList",
		"/getprojectdetail", "ProjectDetail",
		"/deleteproject", "ProjectDelete",
		"/modifyproject", "ProjectModify",
		"/addhost","HostAdd",
		"/listhost","HostList",
		"/gethostdetail","HostDetail",
		"/deletehost","HostDelete",
		"/modifyhost","HostModify",
		"/addvul","VulAdd",
		"/listvul","VulList",
		"/getvuldetail","VulDetail",
		"/deletevul","VulDelete",
		"/modifyvul","VulModify",
		"/addcomment","CommentAdd",
		"/listcomment","CommentList",
		"/getcommentdetail","CommentDetail",
		"/deletecomment","CommentDelete",
		"/modifycomment","CommentModify",
		"/addattachment","AttachmentAdd",
		"/gettaskresult","TaskResultList",
		"/adddict","DictAdd",
		"/getdictlist","DictListEnum",
		"/startdnsbrute","DnsbruteTask")

	app = web.application(urls, globals())
	app.run()


# ================================================主页=========================================

class Index:
	def GET(self):
		render = web.template.render('view')
		return render.index()


class Install:
	def GET(self):
		render = web.template.render('view')
		return render.install()

	def POST(self):
		originParams = web.input()
		options = (
			("dbtype","integer","1-2"),
			("dbhost","string","1-100"),
			("dbport","integer","1-65535"),
			("dbuser","string","1-50"),
			("dbpassword","string","0-50"),
			("dbname","string","1-50"),
		)

		try:
			params = lib.formatParam(originParams, options)
		except lib.ParamError as msg:
			raise web.internalerror("Parameter error, {0}.".format(msg))

		try:
			conf.set("db", "db_type", (params.dbtype=='1' and "mysql" or params.dbtype=='2' and "sqlite"))
			conf.set("db", "db_host", params.dbhost)
			conf.set("db", "db_port", params.dbport)
			conf.set("db", "db_user", params.dbuser)
			conf.set("db", "db_password", params.dbpassword)
			conf.set("db", "db_name", params.dbname)
			conf.write()
			conf.read()
		except WIPError as msg:
			raise web.internalerror("Configure file parse error.")

		try:
			Database.create()
		except DBError as msg:
			raise web.internalerror("Databae creating error.")

		raise web.seeother("/")


# ================================处理project表相关的代码=========================================
class ProjectList:
	def GET(self):
		web.header('Content-Type', 'application/json')
		try:
			result = Project.queryraw('id','name')
		except FieldError as msg:
			raise web.internalerror(msg)
		except WIPError as msg:
			raise web.internalerror("Internal ERROR!")
		else:
			return json.dumps(result)


class ProjectDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')
		params = web.input()
		try:
			project = Project.get(params['id'])
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			project.ctime = str(project.ctime)
			#project.ctime = project.ctime.strftime("%Y-%m-%d %H:%M:%S")
			return project.toJson()


class ProjectAdd:
	def POST(self):
		params = web.input()
		try:
			project = Project(**kw)
			project.save()
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


class ProjectDelete:
	def GET(self):
		params = web.input()
		try:
			project = Project.get(params['id'])
			project.remove()
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


class ProjectModify:
	def POST(self):
		params = web.input()
		try:
			project = Project.get(params.id.strip())
			for key in ("name","url","ip","whois","description"):
				project[key] = params[key].strip()
			project.save(update=True)
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True
		

#=================================处理host表相关的代码=========================================

class HostList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		try:
			result = Host.queryraw('id','title','url','ip','level')
		except FieldError as msg:
			raise web.internalerror(msg)
		except WIPError as msg:
			raise web.internalerror("Internal ERROR!")
		else:
			return json.dumps(result)


class HostDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		params = web.input()
		try:
			result = Host.getraw(params['id'])
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return json.dumps(result)


class HostAdd:
	def POST(self):
		params = web.input()
		try:
			kw = {k:params[k].strip() for k in ("title","url","ip","protocol","level","os","server_info","middleware","description","projectid")}
			Host.insert(**kw)
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


class HostDelete:
	def GET(self):
		params = web.input()
		try:
			Host.delete(params['id'].strip())
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


class HostModify:
	def POST(self):
		params = web.input()
		try:
			kw = {k:params[k].strip() for k in ("title","url","ip","protocol","level","os","server_info","middleware","description")}
			Host.where(id=params['id'].strip()).update(**kw)
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


#=================================处理vul表相关的代码=========================================

class VulList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		try:
			result = Vul.queryraw('id','name','level')
		except FieldError as msg:
			raise web.internalerror(msg)
		except WIPError as msg:
			raise web.internalerror("Internal ERROR!")
		else:
			return json.dumps(result)


class VulDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		params = web.input()
		try:
			result = Vul.getraw(params['id'])
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return json.dumps(result)


class VulAdd:
	def POST(self):
		params = web.input()
		try:
			kw = {k:params[k].strip() for k in ("name","url","info","type","level","description","host_id")}
			Vul.insert(**kw)
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


class VulDelete:
	def GET(self):
		params = web.input()
		try:
			Vul.delete(params['id'].strip())
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


class VulModify:
	def POST(self):
		params = web.input()
		try:
			kw = {k:params[k].strip() for k in ("id","name","url","info","type","level","description")}
			Vul.where(id=params['id'].strip()).update(**kw)
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


#=================================处理comment表相关的代码=========================================

class CommentList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		try:
			result = Comment.queryraw('id','name','level')
		except FieldError as msg:
			raise web.internalerror(msg)
		except WIPError as msg:
			raise web.internalerror("Internal ERROR!")
		else:
			return json.dumps(result)


class CommentDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		params = web.input()
		try:
			result = Comment.getraw(params['id'])
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return json.dumps(result)


class CommentAdd:
	def POST(self):
		params = web.input()
		try:
			kw = {k:params[k].strip() for k in ("name","url","info","level","attachment","description","host_id")}
			Comment.insert(**kw)
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


class CommentDelete:
	def GET(self):
		originParam = web.input()
		options = (("id","integer","0-0"),)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "select attachment from comment where id={0}".format(param.id)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query comment detail failed, reason: {0}.".format(status[1]))
				#print result
				attachment = result[0]['attachment']
				#print attachment
				if attachment != "":
					log.debug(attachment)
					if os.path.exists(os.path.join("static","attachment",attachment)):
						os.remove(os.path.join("static","attachment",attachment))
		
			sqlCmd = "delete from comment where id={0}".format(param.id)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Delete comment detail failed, reason: {0}.".format(status[1]))
				return True


class CommentModify:
	def POST(self):
		params = web.input()
		try:
			kw = {k:params[k].strip() for k in ("name","url","info","level","attachment","description","host_id")}
			Comment.where(id=params['id'].strip()).update(**kw)
		except KeyError:
			raise web.internalerror("Missing argument.")
		except FieldError as msg:
			log.error(msg)
			raise web.internalerror(msg)
		except WIPError as msg:
			log.error(msg)
			raise web.internalerror("Internal ERROR!")
		else:
			return True


#=================================处理attachment表相关的代码=========================================

class AttachmentAdd:
	def POST(self):
		originParam = web.input(attachment={})
		originParam["filename"] = originParam.attachment.filename
		originParam["value"] = originParam.attachment.value

		options = (
			("hostid","integer","0-0"),
			("filename","string","1-200"),
			("name","string","1-200"),
			("value","text","")
		)
			
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			hostID = param.hostid
			attachName = param.name
			attachFilename = param.filename
			fileCTime = time.strftime("%Y-%m-%d-%H%M%S",time.localtime())
			fileNamePrefix = "{0}_{1}".format(hostID,fileCTime)
			if attachName != "":
				attachType = os.path.splitext(attachFilename)[-1]
				fileName = u"{0}_{1}{2}".format(fileNamePrefix,attachName,attachType)
			else:
				fileName = u"{0}_{1}".format(fileNamePrefix,attachFilename)
			fileNameFull = os.path.join("static","attachment",fileName)

			sqlCmd = "insert into comment(name,url,info,level,attachment,description,host_id) values('{0}','{1}'\
				,'{2}','{3}','{4}','{5}','{6}')".format(fileName,"","","3",fileName,"attachment:"+fileName,hostID)

			try:
				fd = open(fileNameFull, "wb")
				#fd.write(param['attachment'].value)
				fd.write(param.value)
			except IOError as msg:
				raise web.internalerror('Write attachment file failed!')
			finally:
				fd.close()

			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Add attachment comment failed, reason: {0}.".format(status[1]))
				return True


#=================================处理domainseek表相关的代码=========================================

class TaskResultList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		originParam = web.input()
		options = (("projectid","integer","0-0"),)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "select id,url,ip,level,source from tmp_host where project_id={0}".format(param.projectid)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query task result failed, reason: {0}.".format(status[1]))
				return lib.queryResultToJson(result)


class DictAdd:
	def POST(self):
		originParam = web.input(dictfile={})

		fileName = param.dictfile.filename
		fileNameFull = os.path.join("plugin","wordlist","dnsbrute",fileName)

		try:
			fd = open(fileNameFull, "w")
			fd.write(param.dictfile.value)
		except IOError as msg:
			raise web.internalerror('Write dictfile failed!')


class DictListEnum:
	def GET(self):
		web.header('Content-Type', 'application/json')

		result = os.listdir(os.path.join("plugin","wordlist","dnsbrute"))

		return json.dumps(result)


class DnsbruteTask:
	def POST(self):
		param = web.data()
		
		paramList = [x.split('=') for x in param.split('&')]
		fileList = [x[1] for x in paramList if x[0]=='dictlist']
		url = [x[1] for x in paramList if x[0]=='url'][0]
		projectID = [x[1] for x in paramList if x[0]=='projectid'][0]

		if url and projectID and fileList:
			dnsbrute = DnsBrute(url,projectID,fileList)
			dnsbrute.start()
		else:
			raise web.internalerror('Dns bruteforce task missing parameter!')

		return True

