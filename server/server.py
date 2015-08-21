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
		"/gettaskstatus","TaskStatus",
		"/gettaskresult","TaskResultList")

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

		result = map(lambda x:zip(("id","name"),x), result)
		result = map(lambda x:dict(x), result)

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
		
		sqlCmd = "select id,url,ip,level from host where project_id = {0} order by {1}".format(param.project_id.strip(),param.orderby.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query host failed!')

		result = map(lambda x:zip(("id","url","ip"),x), result)
		result = map(lambda x:dict(x), result)

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
		nameList = ('id','url','ip','level','os','server_info','middleware','description','project_id')

		return json.dumps(dict(zip(nameList,result)))


class HostAdd:
	def POST(self):
		param = web.input()
		#此处需要校验参数
		
		sqlCmd = "insert into host(url,ip,level,os,server_info,middleware,description,project_id) values('{0}','{1}'\
			,'{2}','{3}','{4}','{5}','{6}','{7}')".format(param.url.strip(),param.ip.strip(),param.level.strip(),\
			param.os.strip(),param.serverinfo.strip(),param.middleware.strip(),param.description.strip(),param.project_id.strip())

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
		
		sqlCmd = "update host set url='{0}',ip='{1}',level='{2}',os='{3}',server_info='{4}',middleware='{5}',description='{6}' \
			where id={7}".format(param.url.strip(),param.ip.strip(),param.level.strip(),param.os.strip(),param.serverinfo.strip(),\
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
		
		sqlCmd = "select id,name from vul where host_id={0} order by {1}".format(param.host_id.strip(),param.orderby.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query vul failed!')

		result = map(lambda x:zip(("id","name"),x), result)
		result = map(lambda x:dict(x), result)

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
			param.level.strip(),param.description.strip(),param.host_id.strip())

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
		
		sqlCmd = "select id,name from comment where host_id={0} order by {1}".format(param.host_id.strip(),param.orderby.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query comment failed!')

		result = map(lambda x:zip(("id","name"),x), result)
		result = map(lambda x:dict(x), result)

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
			param.level.strip(),param.attachment.strip(),param.description.strip(),param.host_id.strip())

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
			
		hostID = param.host_id.strip()
		attachName = param.name.strip()
		attachFilename = param['attachment'].filename.strip()

		fileCTime = time.strftime("%Y-%m-%d-%H%M%S",time.localtime())
		fileNamePrefix = "{0}_{1}".format(hostID,fileCTime)

		if attachName != "":
			attachType = os.path.splitext(attachFilename)[-1]
			fileName = u"{0}_{1}{2}".format(fileNamePrefix,attachName,attachType)
		else:
			fileName = u"{0}_{1}".format(fileNamePrefix,attachFilename)

		sqlCmd = "insert into comment(name,url,info,level,attachment,description,host_id) values('{0}','{1}'\
			,'{2}','{3}','{4}','{5}','{6}')".format(fileName,"","","3",fileName,"attachment:"+fileName,param.host_id.strip())

		try:
			fd = open("static/attachment/"+fileName, "wb")
			fd.write(param['attachment'].value)
		except Exception as msg:
			raise web.internalerror('Add attachment failed!')
		finally:
			fd.close()

		dbcon = DBManage()
		if not dbcon.sql(sqlCmd):
			if os.path.exists("static/attachment/"+fileName):
				os.remove("static/attachment/"+fileName)
			raise web.internalerror('Add attachment comment failed!')

		return True

#=================================处理autotask表相关的代码=========================================

class TaskStatus:
	def GET(self):
		param = web.input()

		sqlCmd = "select * from tmp_task_result_byhost where project_id={0}".format(param.id.strip())
		dbcon = DBManage()
		if not sqlCmd.find(sqlCmd):
			raise web.notfound()

		return True

class TaskResultList:
	def GET(self):
		web.header('Content-Type', 'application/json')
		param = web.input()

		sqlCmd = "select id,url,ip,source from tmp_task_result_byhost where id={0}".format(param.id.strip())
		dbcon = DBManage()
		result = dbcon.find(sqlCmd)
		if not result:
			raise web.internalerror('Query task result failed!')

		columnList = ("id","url","ip","source")
		result = map(lambda x:zip(columnList, x), result)
		result = map(lambda x:dict(x), result)

		return json.dumps(result)