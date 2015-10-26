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

#sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib /Users/apple/.python-eggs/MySQL_python-1.2.5-py2.7-macosx-10.9-intel.egg-tmp/_mysql.so

#=================================================sqlite test============================================

from model.model import Project, Host, Vul, Comment, Database

Database.reset()
#Project.delete(7)
Project.insert(name='dd',url='dd.com',ip='1.1.1.1',level=3,description="ddfuck",whois='ddfuck')

print Project.queryraw()
#Project.create()
#Host.create()
#Vul.create()
#Comment.create()
#Database.create()




