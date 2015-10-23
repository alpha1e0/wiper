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
from thirdparty.BeautifulSoup import BeautifulStoneSoup
from thirdparty.BeautifulSoup import NavigableString#

with open("result.txt", "r") as fd:
	xml = fd.read()

doc = BeautifulStoneSoup(xml)

result = list()

hosts = doc.findAll("host")
for host in hosts:
	if isinstance(host, NavigableString): continue
	state = host.status['state'] # up, down
	ipaddr = host.address['addr'] #1.1.1.1
	#如果没有host，那么hostname没有name属性，这里是否会有问题
	hostname = host.hostnames.hostname['name']
	ports = host.ports.contents
	for port in ports:
		if isinstance(port, NavigableString): continue
		l3type = port['protocol'] #tcp, udp
		portnum = port['portid'] #80, 443
		portstate = port.state['state']# open,close
		protocol = port.service['name']
		result.append(dict(state=state,ipaddr=ipaddr,hostname=hostname,portnum=portnum,l3type=l3type,portstate=portstate,protocol=protocol))

print result

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
