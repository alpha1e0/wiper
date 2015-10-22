#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

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

from thirdparty import yaml

from thirdparty import requests

from thirdparty import web

urls = ("/", "Index")

class Index(object):
	def GET(self):
		return "hello"

app = web.application(urls, globals())
app.run()

#re = requests.get("http://www.baidu.com/baidu?wd=pyyaml&tn=baidulocal")
#print re.text