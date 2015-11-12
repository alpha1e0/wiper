#-*- coding: UTF-8 -*-

import re
from thirdparty import requests

def getTitle(html):
	titlePattern = re.compile(r"(?:<title>)(.*)(?:</title>)")
	charset = None
	charsetPos = html[0:500].lower().find("charset")
	if charsetPos != -1:
		charsetSlice = html[charsetPos:charsetPos+18]
		charsetList = {"utf-8":"utf-8","utf8":"utf-8","gbk":"gbk","gb2312":"gb2312"}
		for key,value in charsetList.iteritems():
			if key in charsetSlice:
				charset = value
				break
	if not charset:
		charset = "utf-8"
	decodedHtml = html.decode(charset)
	match = titlePattern.search(decodedHtml)
	return match.groups()[0] if match else "title not found"

#url = "http://d3.thinksns.com/"
url = "http://www.h3c.com.cn"
titlePattern = re.compile(r"(?:<title>)(.*)(?:</title>)")#

response = requests.get(url)

title = getTitle(response.content)

print title

