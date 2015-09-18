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
from modal.dbmanage import DBManage,SQLQuery,SQLExec
from plugin.dnsbrute import DnsBrute
from init import log


def startServer():
	urls = (
		"/", "Index",
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


# ================================处理project表相关的代码=========================================
class ProjectList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		sqlCmd = "select id,name from project order by 1"
		with SQLQuery(sqlCmd) as (status,result):
			if not status[0]:
				raise web.internalerror("Query project failed, reason: {0}.".format(status[1]))
			return lib.queryResultToJson(result)


class ProjectDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		originParam = web.input()
		options = (("id","integer","0-0"),)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "select * from project where id={0}".format(param.id)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query project detail failed, reason: {0}.".format(status[1]))				
				if result:
					result[0]['ctime'] = result[0]['ctime'].strftime("%Y-%m-%d %H:%M:%S")			
				return lib.queryResultToJson(result)


class ProjectAdd:
	def POST(self):
		originParam = web.input()
		options = (
			("name","string","1-100"),
			("url","url",""),
			("ip","ip",""),
			("whois","text",""),
			("description","text","")
		)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "insert into project(name, url, ip, whois, description) values('{0}', '{1}', '{2}', '{3}', '{4}')".format(\
				param.name, param.url, param.ip, param.whois, param.description)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query project detail failed, reason: {0}.".format(status[1]))			
				return True


class ProjectDelete:
	def GET(self):
		originParam = web.input()
		options = (("id","integer","0-0"),)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))
		
			sqlCmd = "delete from project where id={0}".format(param.id)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Delete project failed, reason: {0}.".format(status[1]))
				return True


class ProjectModify:
	def POST(self):
		originParam = web.input()
		options = (
			("name","string","1-100"),
			("url","url",""),
			("ip","ip",""),
			("whois","text",""),
			("description","text",""),
			("id","integer","0-0")
		)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))		
			sqlCmd = "update project set name='{0}',url='{1}',ip='{2}',whois='{3}',description='{4}' where id={5}".format(\
				param.name, param.url, param.ip, param.whois, param.description, param.id)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Modify project failed, reason: {0}.".format(status[1]))
				return True

#=================================处理host表相关的代码=========================================

class HostList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		originParam = web.input()
		options = (
			("projectid","integer","0-0"),
			("orderby","string","1-20")
		)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))
		
			sqlCmd = "select id,title,url,ip,level from host where project_id = {0} order by {1}".format(param.projectid,param.orderby)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query host failed, reason: {0}.".format(status[1]))
				return lib.queryResultToJson(result)


class HostDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		originParam = web.input()
		options = (("id","integer","0-0"),)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "select * from host where id={0}".format(param.id)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query host detail failed, reason: {0}.".format(status[1]))
				return lib.queryResultToJson(result)


class HostAdd:
	def POST(self):
		originParam = web.input()
		options = (
			("url","url",""),
			("ip","ip",""),
			("title","string","1-200"),
			("protocol","integer","1-20"),
			("level","integer","1-4"),
			("os","string","0-150"),
			("serverinfo","string","0-150"),
			("middleware","string","0-200"),
			("description","text",""),
			("projectid","integer","0-0")
		)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "insert into host(url,ip,title,protocol,level,os,server_info,middleware,description,project_id) values('{0}','{1}'\
				,'{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')".format(param.url,param.ip,param.title,param.protocol,param.level,\
				param.os,param.serverinfo,param.middleware,param.description,param.projectid)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Add host detail failed, reason: {0}.".format(status[1]))
				return True


class HostDelete:
	def GET(self):
		originParam = web.input()
		options = (("id","integer","0-0"),)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "delete from host where id={0}".format(param.id)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Delete host detail failed, reason: {0}.".format(status[1]))
				return True


class HostModify:
	def POST(self):
		originParam = web.input()
		options = (
			("url","url",""),
			("ip","ip",""),
			("title","string","1-200"),
			("protocol","integer","1-20"),
			("level","integer","1-4"),
			("os","string","0-150"),
			("serverinfo","string","0-150"),
			("middleware","string","0-200"),
			("description","text",""),
			("id","integer","0-0")
		)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "update host set url='{0}',ip='{1}',title='{2}',level='{3}',os='{4}',server_info='{5}',middleware='{6}',description='{7}',protocol='{8}' \
				where id={9}".format(param.url,param.ip,param.title,param.level,param.os,param.serverinfo,param.middleware,param.description,param.protocol,param.id)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Modify host detail failed, reason: {0}.".format(status[1]))
				return True


#=================================处理vul表相关的代码=========================================

class VulList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		originParam = web.input()
		options = (
			("hostid","integer","0-0"),
			("orderby","string","1-20")
		)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "select id,name from vul where host_id={0} order by {1}".format(param.hostid,param.orderby)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query vul failed, reason: {0}.".format(status[1]))
				return lib.queryResultToJson(result)


class VulDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		originParam = web.input()
		options = (("id","integer","0-0"),)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))
		
			sqlCmd = "select * from vul where id={0}".format(param.id)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query vul detail failed, reason: {0}.".format(status[1]))
				return lib.queryResultToJson(result)


class VulAdd:
	def POST(self):
		originParam = web.input()
		options = (
			("name","string","1-100"),
			("url","url",""),
			("info","string","0-1024"),
			("type","integer","1-100"),
			("level","integer","1-4"),
			("description","text",""),
			("hostid","integer","0-0")
		)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "insert into vul(name,url,info,type,level,description,host_id) values('{0}','{1}'\
				,'{2}','{3}','{4}','{5}','{6}')".format(param.name,param.url,param.info,param.type,param.level,param.description,param.hostid)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Add vul detail failed, reason: {0}.".format(status[1]))
				return True


class VulDelete:
	def GET(self):
		originParam = web.input()
		options = (("id","integer","0-0"),)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "delete from vul where id={0}".format(param.id)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Delete vul detail failed, reason: {0}.".format(status[1]))
				return True


class VulModify:
	def POST(self):
		originParam = web.input()
		options = (
			("name","string","1-100"),
			("url","url",""),
			("info","string","0-1024"),
			("type","integer","1-100"),
			("level","integer","1-4"),
			("description","text",""),
			("id","integer","0-0")
		)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))
			
			sqlCmd = "update vul set name='{0}',url='{1}',info='{2}',type='{3}',level='{4}',description='{5}'\
				where id={6}".format(param.name,param.url,param.info,param.type,param.level,param.description,param.id)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Modify vul detail failed, reason: {0}.".format(status[1]))
				return True


#=================================处理comment表相关的代码=========================================

class CommentList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		originParam = web.input()
		options = (
			("hostid","integer","0-0"),
			("orderby","string","1-20")
		)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "select id,name from comment where host_id={0} order by {1}".format(param.hostid,param.orderby)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query comment failed, reason: {0}.".format(status[1]))
				return lib.queryResultToJson(result)


class CommentDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		originParam = web.input()
		options = (("id","integer","0-0"),)

		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))
		
			sqlCmd = "select * from comment where id={0}".format(param.id)
			with SQLQuery(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Query comment detail failed, reason: {0}.".format(status[1]))
				return lib.queryResultToJson(result)


class CommentAdd:
	def POST(self):
		originParam = web.input()
		options = (
			("name","string","1-100"),
			("url","url",""),
			("info","string","0-1024"),
			("level","integer","1-4"),
			("attachment","string","0-200"),
			("description","text",""),
			("hostid","integer","0-0")
		)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "insert into comment(name,url,info,level,attachment,description,host_id) values('{0}','{1}'\
				,'{2}','{3}','{4}','{5}','{6}')".format(param.name,param.url,param.info,param.level,param.attachment,param.description,param.hostid)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Add comment detail failed, reason: {0}.".format(status[1]))
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
		originParam = web.input()
		options = (
			("name","string","1-100"),
			("url","url",""),
			("info","string","0-1024"),
			("level","integer","1-4"),
			("attachment","string","0-200"),
			("description","text",""),
			("id","integer","0-0")
		)
		
		with lib.ParamCheck(originParam, options) as (status,param):
			if not status[0]:
				raise web.internalerror("Parameter check error, reason: {0}".format(status[1]))

			sqlCmd = "update comment set name='{0}',url='{1}',info='{2}',level='{3}',attachment='{4}',description='{5}' \
				where id={6}".format(param.name,param.url,param.info,param.level,param.attachment,param.description,param.id)
			with SQLExec(sqlCmd) as (status,result):
				if not status[0]:
					raise web.internalerror("Modify comment detail failed, reason: {0}.".format(status[1]))
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

