#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


#=================================================searchengine test===========================================
#from plugin.lib.searchengine import Query

#['site','title','url','filetype','link','kw']

#query = Query(filetype="xls") | Query(site="huawei.com")
#query = Query(title="torrent")
#query = Query(filetype="xls")
#print query.genKeyword("bing")
#query = Query(kw="siw")
#re = query.doSearch(engine="bing", size=5)
#print re
#for line in re:
#	print line[0]
#	print line[1]
#	print line[2]


#=================================================nmap test===========================================
#from subprocess import Popen, PIPE, STDOUT

#from plugin.lib.nmapwrapper import Nmap

#result = Nmap.scan("nmap -n 192.168.1.1/24")

#for l in result: print l

#=================================================dnsresolver test============================================
#from plugin.lib.dnsresolve import DnsResolver

#dns = DnsResolver()
#re = dns.getRecords("ns","www.baidu.com")
#re = dns.resolveAll("baidu.com")
#re = dns.getZoneRecords("thinksns.com")
#print re


#=================================================sqlite test============================================

#from model.model import Project, Host, Vul, Comment, Database

#Database.reset()
##Project.delete(7)
#Project.insert(name='dd',url='dd.com',ip='1.1.1.1',level=3,description="ddfuck",whois='ddfuck')#

#print Project.queryraw()
#print dir(Project)

#Project.create()
#Host.create()
#Vul.create()
#Comment.create()
#Database.create()


#=================================================plugin framework test============================================
from multiprocessing import Manager, freeze_support
import time

import config

from plugin.lib.plugin import Plugin
from plugin.datasave import DataSave
from plugin.dnsbrute import DnsBrute
from plugin.googlehacking import GoogleHacking
from plugin.serviceidentify import ServiceIdentify
from plugin.subnetscan import SubnetScan
from plugin.zonetrans import ZoneTrans

from model.model import Host


class plu(Plugin):
	def __init__(self, namestr):
		self.namestr = namestr
		super(plu,self).__init__(timeout=1)
	def handle(self, data):
		print "debug: " + self.name + " got " + data.description
		data.description = self.namestr + "handle"
		self.put(data)

class end(Plugin):
	def __init__(self, namestr):
		self.namestr = namestr
		super(end,self).__init__(timeout=1)
	def handle(self, data):
		print "debug: " + self.name + " got " + data.description
		pass

#host = Host()
#host.description = "init host"#

#aa = plu('aa')
#bb = plu('bb')
#cc = plu('cc')
#dd = plu('dd')
#ee = plu('ee')
#zz = end('zz')#

#p = cc | (aa + bb) | zz
##p = aa | zz
##p = zz
##print zz.namestr
#print [x.name for x in p._addList]
#print [x.name for x in p._orList]
#print "-----------------------------"



if __name__ == '__main__':
	#config.RTD.log = config.Log()
	config.RTD.taskManager = Manager()


	host = Host()
	#host.url = "baidu.com"
	host.url = "thinksns.com"
	host.ip = "61.164.118.174"
	#host.ip = "61.164.118.4"
	#host.url = "xiuren.com"

	#p = ZoneTrans() | DataSave(1,1)
	#p = DnsBrute(["test.txt"]) | DataSave(1,1)
	#p = GoogleHacking() | DataSave(1,1)
	#p = SubnetScan() | DataSave(1,1)
	#p = ServiceIdentify() | DataSave(1,1)
	google = GoogleHacking()
	dns = DnsBrute(["test"])
	zone = ZoneTrans()
	sub = SubnetScan()
	serv = ServiceIdentify()
	data = DataSave(1,1)

	#p = (zone + google
	#p = (dns + google + zone) | serv | data
	p = google | serv | data
	#p = (GoogleHacking() + DnsBrute(["test"]) + ZoneTrans() + SubnetScan()) | ServiceIdentify() | DataSave(1,1)
	p.dostart([host])

	time.sleep(6000)



