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
import web
import json

from dbman.dbmanage import DBManage
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


class Index:
	def GET(self):
		index = web.template.frender('server/index.html')

		return index()

# ================================处理project表相关的代码=========================================
class ProjectList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		sqlCmd = "select id,name from project order by 1"
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query project failed!')

		result = [zip(("id","name"),x) for x in result]
		result = [dict(x) for x in result]

		return json.dumps(result)


class ProjectDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		param = web.input()
		#此处需要校验参数

		sqlCmd = "select * from project where id={0}".format(param.id.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror("Query project detail failed!")

		result = list(result[0])
		result[5] = result[5].strftime("%Y-%m-%d %H:%M:%S")
		nameList = ('id','name','url','ip','whois','ctime','description')

		return json.dumps(dict(zip(nameList,result)))


class ProjectAdd:
	def POST(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "insert into project(name, url, ip, whois, description) values('{0}', '{1}', '{2}', '{3}', '{4}')".format(\
			param.name.strip(), param.url.strip(), param.ip.strip(), param.whois.strip(), param.description.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Add project failed!')
		
		return True


class ProjectDelete:
	def GET(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "delete from project where id={0}".format(param.id.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror("Delete project failed!")

		return True


class ProjectModify:
	def POST(self):
		#此处需要校验参数
		
		param = web.input()
		sqlCmd = "update project set name='{0}',url='{1}',ip='{2}',whois='{3}',description='{4}' where id={5}".format(\
			param.name.strip(), param.url.strip(), param.ip.strip(), param.whois.strip(), param.description.strip(), param.id.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Modify project failed!')
		
		return True

#=================================处理host表相关的代码=========================================

class HostList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "select id,url,ip,level from host where project_id = {0} order by {1}".format(param.projectid.strip(),param.orderby.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query host failed!')

		result = [zip(("id","url","ip"),x) for x in result]
		result = [dict(x) for x in result]

		return json.dumps(result)


class HostDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "select * from host where id={0}".format(param.id.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror("Query host detail failed!")

		result = list(result[0])
		nameList = ('id','url','ip','title','level','os','server_info','middleware','description','project_id')

		return json.dumps(dict(zip(nameList,result)))


class HostAdd:
	def POST(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "insert into host(url,ip,title,level,os,server_info,middleware,description,project_id) values('{0}','{1}'\
			,'{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(param.url.strip(),param.ip.strip(),param.title.strip(),param.level.strip(),\
			param.os.strip(),param.serverinfo.strip(),param.middleware.strip(),param.description.strip(),param.projectid.strip())

		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Add host failed!')

		return True


class HostDelete:
	def GET(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "delete from host where id={0}".format(param.id.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror("Delete host failed!")

		return True


class HostModify:
	def POST(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "update host set url='{0}',ip='{1}',title='{2}',level='{3}',os='{4}',server_info='{5}',middleware='{6}',description='{7}' \
			where id={8}".format(param.url.strip(),param.ip.strip(),param.title.strip(),param.level.strip(),param.os.strip(),param.serverinfo.strip(),\
			param.middleware.strip(),param.description.strip(),param.id.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Modify host failed!')
		
		return True

#=================================处理vul表相关的代码=========================================

class VulList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		param = web.input()#此处需要校验参数
		
		sqlCmd = "select id,name from vul where host_id={0} order by {1}".format(param.hostid.strip(),param.orderby.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query vul failed!')

		result = [zip(("id","name"),x) for x in result]
		result = [dict(x) for x in result]

		return json.dumps(result)


class VulDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "select * from vul where id={0}".format(param.id.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror("Query vul detail failed!")

		result = list(result[0])
		nameList = ('id','name','url','info','type','level','description','host_id')

		return json.dumps(dict(zip(nameList,result)))


class VulAdd:
	def POST(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "insert into vul(name,url,info,type,level,description,host_id) values('{0}','{1}'\
			,'{2}','{3}','{4}','{5}','{6}')".format(param.name.strip(),param.url.strip(),param.info.strip(),param.type.strip(),
			param.level.strip(),param.description.strip(),param.hostid.strip())

		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Add vul failed!')

		return True


class VulDelete:
	def GET(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "delete from vul where id={0}".format(param.id.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror("Delete vul failed!")

		return True


class VulModify:
	def POST(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "update vul set name='{0}',url='{1}',info='{2}',type='{3}',level='{4}',description='{5}' \
			where id={6}".format(param.name.strip(),param.url.strip(),param.info.strip(),param.type.strip(),param.level.strip(),
			param.description.strip(),param.id.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Modify vul failed!')
		
		return True

#=================================处理comment表相关的代码=========================================

class CommentList:
	def GET(self):
		web.header('Content-Type', 'application/json')

		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "select id,name from comment where host_id={0} order by {1}".format(param.hostid.strip(),param.orderby.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query comment failed!')

		result = [zip(("id","name"),x) for x in result]
		result = [dict(x) for x in result]

		return json.dumps(result)


class CommentDetail:
	def GET(self):
		web.header('Content-Type', 'application/json')

		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "select * from comment where id={0}".format(param.id.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror("Query comment detail failed!")

		result = list(result[0])
		nameList = ('id','name','url','info','level','attachment','description','host_id')

		return json.dumps(dict(zip(nameList,result)))


class CommentAdd:
	def POST(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "insert into comment(name,url,info,level,attachment,description,host_id) values('{0}','{1}'\
			,'{2}','{3}','{4}','{5}','{6}')".format(param.name.strip(),param.url.strip(),param.info.strip(),
			param.level.strip(),param.attachment.strip(),param.description.strip(),param.hostid.strip())

		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Add comment failed!')

		return True


class CommentDelete:
	def GET(self):
		param = web.input()
		#此处需要校验参数

		queryCmd = "select attachment from comment where id={0}".format(param.id.strip())
		dbcon = DBManage()
		result = dbcon.find(queryCmd)
		if not result:
			raise web.internalerror("Query comment detail failed!")

		attachment = result[0][0]
		print attachment
		if attachment != "":
			if os.path.exists("static/attachment/"+attachment):
				os.remove("static/attachment/"+attachment)
		
		sqlCmd = "delete from comment where id={0}".format(param.id.strip())
		if not dbcon.sql(sqlCmd):
			raise web.internalerror("Delete comment failed!")

		return True


class CommentModify:
	def POST(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "update comment set name='{0}',url='{1}',info='{2}',level='{3}',attachment='{4}',description='{5}' \
			where id={6}".format(param.name.strip(),param.url.strip(),param.info.strip(),param.level.strip(),
			param.attachment.strip(),param.description.strip(),param.id.strip())
		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			raise web.internalerror('Modify comment failed!')
		
		return True


#=================================处理attachment表相关的代码=========================================

class AttachmentAdd:
	def POST(self):
		param = web.input(attachment={})
		#此处需要校验参数
			
		hostID = param.hostid.strip()
		attachName = param.name.strip()
		attachFilename = param['attachment'].filename.strip()

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
			#fd = open("static/attachment/"+fileName, "wb")
			fd = open(fileNameFull, "wb")
			fd.write(param['attachment'].value)
		except IOError as msg:
			raise web.internalerror('Add attachment failed!')
		finally:
			fd.close()

		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			if os.path.exists(fileNameFull):
				os.remove(fileNameFull)
			raise web.internalerror('Add attachment comment failed!')

		return True

#=================================处理autotask表相关的代码=========================================

class TaskResultList:
	def GET(self):
		web.header('Content-Type', 'application/json')
		param = web.input()
		#此处需要校验参数

		sqlCmd = "select id,url,ip,level,source from tmp_task_result_byhost where project_id={0}".format(param.projectid.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query task result failed!')

		columnList = ("id","url","ip","level","source")
		result = [zip(columnList, x) for x in result]
		result = [dict(x) for x in result]

		return json.dumps(result)

class DictAdd:
	def POST(self):
		param = web.input(dictfile={})

		fileName = param['dictfile'].filename.strip()
		fileNameFull = os.path.join("plugin","wordlist","dnsbrute",fileName)

		try:
			fd = open(fileNameFull, "w")
			fd.write(param['dictfile'].value)
		except IOError as msg:
			raise web.internalerror('Add attachment failed!')

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
			raise web.internalerror('Missing argument!')

		return True

