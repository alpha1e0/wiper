#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''


import sys
import os
import time
import json

from thirdparty import web

from lib import formatParam, ParamError, handleException, jsonSuccess, jsonFail
from model.orm import FieldError, ModelError
from model.model import Database, Project, Host, Vul, Comment
from model.dbmanage import DBError
from config import RTD, CONF, WIPError
from plugin.datasave import DataSave
from plugin.dnsbrute import DnsBrute
from plugin.googlehacking import GoogleHacking
from plugin.serviceidentify import ServiceIdentify
from plugin.subnetscan import SubnetScan
from plugin.zonetrans import ZoneTrans


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
		"/startdnsbrute","DnsbruteTask",
		"/test","Test")

	app = web.application(urls, globals())
	app.run()

	
class Test:
	def GET(self):
		host = Host()
		host.url = "thinksns.com"
		host.ip = "61.164.118.174"

		google = GoogleHacking()
		dns = DnsBrute(["test"])
		zone = ZoneTrans()
		sub = SubnetScan()
		serv = ServiceIdentify()
		data = DataSave(1,1)

		p = google | serv | data
		p.dostart([host])

# ================================================index page=========================================

class Index:
	def GET(self):
		render = web.template.render('view')
		if not CONF.isinstall:
			return render.install()
		else:
			return render.index()


class Install:
	def GET(self):
		render = web.template.render('view')
		if CONF.isinstall:
			return render.index()
		else:
			return render.install()

	def POST(self):
		originParams = web.input()
		options = (
			("dbname","string","1-50"),
		)

		try:
			params = formatParam(originParams, options)
		except ParamError as error:
			raise web.internalerror("Parameter error, {0}.".format(error))

		try:
			CONF.db.name = str(params.dbname)
		except WIPError as error:
			raise web.internalerror("Configure file parse error.")

		try:
			Database.create()
		except DBError as error:
			raise web.internalerror("Databae creating error,"+str(error))

		CONF.isinstall = True
		CONF.save()

		if not os.path.exists("log"):
			os.mkdir("log")
		if not os.path.exists(os.path.join("static","attachment")):
			os.mkdir(os.path.join("static","attachment"))
		if not os.path.exists("data"):
			os.mkdir("data")

		return jsonSuccess()


# ================================the operation of project=========================================
class ProjectList:
	@handleException
	def GET(self):
		params = web.input()
		result = Project.orderby(params.orderby.strip()).getsraw("id","name","level")
		return json.dumps(result)


class ProjectDetail:
	@handleException
	def GET(self):
		params = web.input()
		project = Project.get(params.id)
		return project.toJson()


class ProjectAdd:
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("name","url","ip","level","whois","description")}
		project = Project(**kw)
		project.save()
		return jsonSuccess()


class ProjectDelete:
	@handleException
	def GET(self):
		params = web.input()
		project = Project.get(params.id)
		project.remove()
		return jsonSuccess()


class ProjectModify:
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("name","url","ip","whois","description")}
		Project.where(id=params.id.strip()).update(**kw)
		return jsonSuccess()
		

#=================================the operation of host=========================================

class HostList:
	@handleException
	def GET(self):
		params = web.input()
		result = Host.where(project_id=params.projectid.strip()).orderby(params.orderby.strip()).getsraw('id','title','url','ip','level','protocol')
		return json.dumps(result)


class HostDetail:
	@handleException
	def GET(self):
		params = web.input()
		result = Host.getraw(params.id)
		return json.dumps(result)


class HostAdd:
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("title","url","ip","port","protocol","level","os","server_info","middleware","description","project_id")}
		Host.insert(**kw)
		return jsonSuccess()


class HostDelete:
	@handleException
	def GET(self):
		params = web.input()
		Host.delete(params.id.strip())
		return jsonSuccess()


class HostModify:
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("title","url","ip","port","protocol","level","os","server_info","middleware","description")}
		Host.where(id=params.id.strip()).update(**kw)
		return jsonSuccess()


#=================================the operation of vul=========================================

class VulList:
	@handleException
	def GET(self):
		params = web.input()
		result = Vul.where(host_id=params.hostid.strip()).orderby(params.orderby.strip()).getsraw('id','name','level')
		return json.dumps(result)


class VulDetail:
	@handleException
	def GET(self):
		params = web.input()
		result = Vul.getraw(params.id)
		return json.dumps(result)


class VulAdd:
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("name","url","info","type","level","description","host_id")}
		Vul.insert(**kw)
		return jsonSuccess()


class VulDelete:
	@handleException
	def GET(self):
		params = web.input()
		Vul.delete(params.id.strip())
		return jsonSuccess()


class VulModify:
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("id","name","url","info","type","level","description")}
		Vul.where(id=params.id.strip()).update(**kw)
		return jsonSuccess()


#=================================the operation of comment=========================================

class CommentList:
	@handleException
	def GET(self):
		params = web.input()
		result = Comment.where(host_id=params.hostid.strip()).orderby(params.orderby.strip()).getsraw('id','name','level')
		return json.dumps(result)		


class CommentDetail:
	@handleException
	def GET(self):
		params = web.input()
		result = Comment.getraw(params.id)
		return json.dumps(result)


class CommentAdd:
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("name","url","info","level","description","host_id")}
		Comment.insert(**kw)
		return jsonSuccess()


class CommentDelete:
	def GET(self):
		params = web.input()

		try:
			comment = Comment.get(params.id.strip())
		except AttributeError:
			raise web.internalerror("Missing parameter.")
		except FieldError as error:
			raise web.internalerror(error)
		except WIPError as error:
			RTD.log.error(error)
			raise web.internalerror("Internal ERROR!")

		if not comment:
			return jsonFail()

		#delete attachment
		if comment.attachment:
			if os.path.exists(os.path.join("static","attachment",comment.attachment)):
				os.remove(os.path.join("static","attachment",comment.attachment))

		comment.remove()

		return jsonSuccess()


class CommentModify:
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("id","name","url","info","level","description")}
		Comment.where(id=params.id.strip()).update(**kw)
		return jsonSuccess()


class AttachmentAdd:
	def POST(self):
		originParams = web.input(attachment={})
		originParams["filename"] = originParams.attachment.filename
		originParams["value"] = originParams.attachment.value

		options = (
			("hostid","integer","0-0"),
			("filename","string","1-200"),
			("name","string","0-200"),
			("value","text","")
		)

		try:
			params = formatParam(originParams, options)
		except ParamError as error:
			raise web.internalerror("Parameter error, {0}.".format(error))
			

		hostID = params.hostid
		attachName = params.name
		attachFilename = params.filename
		fileCTime = time.strftime("%Y-%m-%d-%H%M%S",time.localtime())
		fileNamePrefix = "{0}_{1}".format(hostID,fileCTime)
		if attachName != "":
			attachType = os.path.splitext(attachFilename)[-1]
			fileName = u"{0}_{1}{2}".format(fileNamePrefix,attachName,attachType)
		else:
			fileName = u"{0}_{1}".format(fileNamePrefix,attachFilename)
		fileNameFull = os.path.join("static","attachment",fileName)

		try:
			comment = Comment(name=fileName,url="",info="",level=3,attachment=fileName,description="attachment:"+fileName,host_id=hostID)
		except WIPError as error:
			RTD.log.error(error)
			raise web.internalerror("Internal ERROR!")

		try:
			fd = open(fileNameFull, "wb")
			fd.write(params.value)
		except IOError as error:
			raise web.internalerror('Write attachment file failed!')
		finally:
			fd.close()

		try:
			comment.save()
		except FieldError as error:
			RTD.log.error(error)
			raise web.internalerror(error)
		except WIPError as error:
			RTD.log.error(error)
			raise web.internalerror("Internal ERROR!")

		return True


#=================================operation of domainseek=========================================

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

		try:
			fileName = param.dictfile.filename
		except AttributeError:
			raise web.internalerror("Missing parameter.")
		fileNameFull = os.path.join("plugin","wordlist","dnsbrute",fileName)

		try:
			fd = open(fileNameFull, "w")
			fd.write(param.dictfile.value)
		except IOError as error:
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

