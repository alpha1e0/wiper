#!/usr/bin/env python
#-*- coding: UTF-8 -*-


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

import subprocess
from thirdparty.BeautifulSoup import BeautifulStoneSoup

with open("result.txt", "r") as fd:
	xml = fd.read()

doc = BeautifulStoneSoup(xml)




