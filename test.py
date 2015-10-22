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
#from thirdparty.BeautifulSoup import BeautifulStoneSoup#

##with open("result.txt", "r") as fd:
##	xml = fd.read()##

##doc = BeautifulStoneSoup(xml)
#cmd = "nmap -A 192.168.13.129 -oX -"
#p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
#print "first"
##p.wait()
#print "second"
#print p.stdout.read()


#=================================================dnsresolver test============================================
#from plugin.lib.dnsresolve import DnsResolver

#dns = DnsResolver()
#re = dns.getRecords("ns","www.baidu.com")
#re = dns.resolveAll("baidu.com")
#re = dns.getZoneRecords("thinksns.com")
#print re
