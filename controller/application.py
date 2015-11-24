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
		"/subdomainscan","SubDomianScan",
		"/subnetscan","SubNetScan",
		"/savetmphost","SaveTmpHost",
		"/deletetmphost","DeleteTmpHost",
		"/servicerecognize","ServiceRecognize",
		"/dbsetup","DBSetup",
		"/adddict","DictAdd",
		"/nmapsetup","NmapSetup"
	)


	app = web.application(urls, globals())
	app.run()


# ================================================index page=========================================

class Index(object):
	def GET(self):
		render = web.template.render('view')
		if not CONF.isinstall:
			return render.install()
		else:
			return render.index()


class Install(object):
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
		if not os.path.exists(os.path.join("data","database")):
			os.mkdir(os.path.join("data","database"))

		return jsonSuccess()


# ================================the operation of project=========================================
class ProjectList(object):
	@handleException
	def GET(self):
		params = web.input()
		result = Project.orderby(params.orderby.strip()).getsraw("id","name","level")
		return json.dumps(result)


class ProjectDetail(object):
	@handleException
	def GET(self):
		params = web.input()
		project = Project.get(params.id)
		return project.toJson()


class ProjectAdd(object):
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("name","url","ip","level","whois","description")}
		project = Project(**kw)
		project.save()
		return jsonSuccess()


class ProjectDelete(object):
	@handleException
	def GET(self):
		params = web.input()
		project = Project.get(params.id)
		project.remove()
		return jsonSuccess()


class ProjectModify(object):
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("name","url","ip","whois","description","level")}
		Project.where(id=params.id.strip()).update(**kw)
		return jsonSuccess()
		

#=================================the operation of host=========================================

class HostList(object):
	@handleException
	def GET(self):
		params = web.input()
		result = Host.where(project_id=params.projectid.strip()).orderby(params.orderby.strip()).getsraw('id','title','url','ip','level','protocol')
		return json.dumps(result)


class HostDetail(object):
	@handleException
	def GET(self):
		params = web.input()
		result = Host.getraw(params.id)
		return json.dumps(result)


class HostAdd(object):
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("title","url","ip","port","protocol","level","os","server_info","middleware","description","project_id")}
		Host.insert(**kw)
		return jsonSuccess()


class HostDelete(object):
	@handleException
	def GET(self):
		params = web.input()
		Host.delete(params.id.strip())
		return jsonSuccess()


class HostModify(object):
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("title","url","ip","port","protocol","level","os","server_info","middleware","description")}
		Host.where(id=params.id.strip()).update(**kw)
		return jsonSuccess()


#=================================the operation of vul=========================================

class VulList(object):
	@handleException
	def GET(self):
		params = web.input()
		result = Vul.where(host_id=params.hostid.strip()).orderby(params.orderby.strip()).getsraw('id','name','level')
		return json.dumps(result)


class VulDetail(object):
	@handleException
	def GET(self):
		params = web.input()
		result = Vul.getraw(params.id)
		return json.dumps(result)


class VulAdd(object):
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("name","url","info","type","level","description","host_id")}
		Vul.insert(**kw)
		return jsonSuccess()


class VulDelete(object):
	@handleException
	def GET(self):
		params = web.input()
		Vul.delete(params.id.strip())
		return jsonSuccess()


class VulModify(object):
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("id","name","url","info","type","level","description")}
		Vul.where(id=params.id.strip()).update(**kw)
		return jsonSuccess()


#=================================the operation of comment=========================================

class CommentList(object):
	@handleException
	def GET(self):
		params = web.input()
		result = Comment.where(host_id=params.hostid.strip()).orderby(params.orderby.strip()).getsraw('id','name','level')
		return json.dumps(result)		


class CommentDetail(object):
	@handleException
	def GET(self):
		params = web.input()
		result = Comment.getraw(params.id)
		return json.dumps(result)


class CommentAdd(object):
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("name","url","info","level","description","host_id")}
		Comment.insert(**kw)
		return jsonSuccess()


class CommentDelete(object):
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


class CommentModify(object):
	@handleException
	def POST(self):
		params = web.input()
		kw = {k:params[k].strip() for k in ("id","name","url","info","level","description")}
		Comment.where(id=params.id.strip()).update(**kw)
		return jsonSuccess()


class AttachmentAdd(object):
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


#=================================operation of autotask=========================================

class SubDomianScan(object):
	def GET(self):
		web.header('Content-Type', 'application/json')

		result = os.listdir(os.path.join("data","wordlist","dnsbrute"))
		return json.dumps(result)

	def POST(self):
		web.header('Content-Type', 'application/json')
		params = web.input()
		rawParam = web.data()

		try:
			projectid = int(params.project_id)
		except AttributeError as error:
			RTD.log.error(error)
			raise web.internalerror(error)

		rawParamList = [x.split("=") for x in rawParam.split("&")]
		dictList = [x[1] for x in rawParamList if x[0]=="dictlist"]

		task = None
		if "dnsbrute" in params.keys():
			task = DnsBrute(dictList)
		if "googlehacking" in params.keys():
			task = (task + GoogleHacking()) if task else GoogleHacking()
		if "zonetrans" in params.keys():
			task = (task + ZoneTrans()) if task else ZoneTrans()

		task = task | ServiceIdentify() | DataSave(projectid=projectid)

		host = Host(url=params.domain)
		task.dostart([host])
		print "debug: host addlist",task._addList
		print "debug: host orlist",task._orList

		return jsonSuccess()


class SubNetScan(object):
	def getIPList(self, projectid):
		try:
			hosts = Host.where(project_id=projectid).getsraw("ip")
		except (KeyError, AttributeError, FieldError, ModelError, DBError) as error:
			RTD.log.error(error)
			raise web.internalerror(error)
		
		result = list()
		for host in hosts:
			try:
				pos = host['ip'].rindex(".")
				ip = host['ip'][:pos] + ".1"
			except (KeyError, ValueError, AttributeError):
				continue
			for key in result:
				if ip == key[0]:
					key[1] += 1
					break
			else:
				result.append([ip,1])

		return result

	def GET(self):
		web.header('Content-Type', 'application/json')
		params = web.input()

		try:
			projectid = int(params.project_id)
		except AttributeError as error:
			RTD.log.error(error)
			raise web.internalerror(error)

		iplist = self.getIPList(projectid)
		hosts = Host.where(project_id=projectid, tmp=1).orderby("ip").getsraw('id','title','ip','port','protocol')

		result = {'iplist':iplist, 'hosts':hosts}

		return json.dumps(result)

	def POST(self):
		web.header('Content-Type', 'application/json')
		params = web.input()
		rawParam = web.data()

		try:
			projectid = int(params.project_id)
		except AttributeError as error:
			RTD.log.error(error)
			raise web.internalerror(error)

		rawParamList = [x.split("=") for x in rawParam.split("&")]
		ipList = [x[1] for x in rawParamList if x[0]=="iplist"]

		hosts = [Host(ip=x) for x in ipList]
		defaultValue = {"tmp":1}
		task = SubnetScan() | ServiceIdentify(ptype=1) | DataSave(defaultValue=defaultValue,projectid=projectid)
		task.dostart(hosts)

		return jsonSuccess()


class SaveTmpHost(object):
	def GET(self):
		web.header('Content-Type', 'application/json')
		params = web.input()

		try:
			hid = str(int(params.id))
		except AttributeError as error:
			RTD.log.error(error)
			raise web.internalerror(error)

		try:
			host = Host.get(hid)
			host.tmp = 0
			host.save(update=True)
		except (KeyError, AttributeError, FieldError, ModelError, DBError) as error:
			RTD.log.error(error)
			raise web.internalerror(error)

		return jsonSuccess()


class DeleteTmpHost(object):
	def GET(self):
		web.header('Content-Type', 'application/json')
		params = web.input()

		try:
			hid = str(int(params.id))
		except AttributeError as error:
			RTD.log.error(error)
			raise web.internalerror(error)

		try:
			Host.delete(hid)
		except (KeyError, AttributeError, FieldError, ModelError, DBError) as error:
			RTD.log.error(error)
			raise web.internalerror(error)

		return jsonSuccess()


class ServiceRecognize(object):
	def POST(self):
		web.header('Content-Type', 'application/json')
		originParams = web.input()

		options = (
			("domain","string","1-200"),
			("type","integer","0-3"),
			("project_id","integer","")
		)
		try:
			params = formatParam(originParams, options)
		except ParamError as error:
			raise web.internalerror("Parameter error, {0}.".format(error))

		domain = params.domain.lower()
		protocol = ""
		port = None

		#resolve protocol
		if domain.startswith("http://"):
			protocol = "http"
			domain = domain[7:]
			port = 80
		elif domain.startswith("https://"):
			protocol = "https"
			domain = domain[8:]
			port = 443
		elif "://" in domain:
			raise web.internalerror("unrecognized protocol, should be 'http' or 'https'.")
		#resolve port
		try:
			pos = domain.rindex(":")
		except ValueError:
			pass
		else:
			try:
				port = int(domain[pos+1:])
			except ValueError:
				pass
			domain = domain[:pos]

		if not protocol: protocol = "http"
		if not port: port = 80

		task = ServiceIdentify(ptype=int(params.type)) | DataSave(projectid=params.project_id)
		host = Host(url=domain,protocol=protocol,port=port)
		task.dostart([host])

		return jsonSuccess()


class DBSetup(object):
	def GET(self):
		web.header('Content-Type', 'application/json')

		result = os.listdir(os.path.join("data","database"))
		return json.dumps(result)

	def POST(self):
		web.header('Content-Type', 'application/json')
		originParams = web.input()

		options = (
			("database","string","1-50"),
		)
		try:
			params = formatParam(originParams, options)
		except ParamError as error:
			raise web.internalerror("Parameter error, {0}.".format(error))

		oldDB = CONF.db.name
		CONF.db.name = str(params.database)
		dblist = os.listdir(os.path.join("data","database"))
		if params.database not in dblist:
			try:
				Database.create()
			except DBError as error:
				CONF.db.name = oldDB
				raise web.internalerror("Databae creating error,"+str(error))
		CONF.save()

		return jsonSuccess()


class DictAdd(object):
	def POST(self):
		web.header('Content-Type', 'application/json')
		params = web.input(dictfile={})

		try:
			fileName = params.dictfile.filename
			dtype = int(params.type)
		except AttributeError:
			raise web.internalerror("Missing parameter.")
		if dtype == 0:
			fileNameFull = os.path.join("data","wordlist","dnsbrute",fileName)
		else:
			raise web.internalerror("dict type error.")

		try:
			fd = open(fileNameFull, "w")
			fd.write(params.dictfile.value)
		except IOError as error:
			raise web.internalerror('Write dictfile failed!')

		return jsonSuccess()


class NmapSetup(object):
	def POST(self):
		originParams = web.input()

		options = (
			("nmappath","string","1-200"),
		)
		try:
			params = formatParam(originParams, options)
		except ParamError as error:
			raise web.internalerror("Parameter error, {0}.".format(error))

		CONF.nmap = None if str(params.nmappath)=="nmap" else str(params.nmappath)
		CONF.save()

		return jsonSuccess()

