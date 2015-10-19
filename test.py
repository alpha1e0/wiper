#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import os
import random
import time
import urllib

import requests
import yaml
from thirdparty.BeautifulSoup import BeautifulSoup


class SearchEngineError(Exception):
	def __init__(self, reason=""):
		self.errMsg = "SearchEngineError. " + ("reason: "+reason if reason else "")

	def __str__(self):
		return self.errMsg


class SearchConfig(object):
	def __new__(cls, engine):
		configFile = os.path.join("plugin","config","searchengine.yaml")
		try:
			with open(configFile, "r") as fd:
				config = yaml.load(fd)[engine]
		except IOError:
			raise SearchEngineError("read searchengine configuration file 'searchengine.yaml' failed")
		else:
			return config


class UserAgents(object):
	def __new__(cls):
		configFile = os.path.join("plugin","config","useragent.yaml")
		try:
			with open(configFile, "r") as fd:
				config = yaml.load(fd)
		except IOError:
			userAgents = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
				"Mozilla/5.0 (Windows; U; Windows NT 5.2)Gecko/2008070208 Firefox/3.0.1",
				"Opera/9.27 (Windows NT 5.2; U; zh-cn)",
				"Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en)Opera 8.0)"]
		else:
			userAgents = [x['User-Agent'] for x in config]

		return userAgents


def genUrlParam(key, value, **kwargs):
	'''
	Generate the url parameters
	input:
		key: the key of url parameter
		value: the value of url parameter
		kwargs: if this parameter specified, the function will ignore the first two parameter
	'''
	if kwargs:
		return "&".join([k+"="+v for k,v in kwargs.iteritems()]) + "&"
	else:
		return key + "=" + str(value) + "&"


class Query(object):
	'''
	Build query keyword
	input:
		site: seach specified site
		title: search in title
		url: search in url
		filetype: search files with specified file type
		link: search in link
		kw: raw keywords to search 
	example:
		query = Query(site="xxx.com") | -Query(site="www.xxx.com") | Query(kw="password")
		query.doSearch(engine="baidu")
	'''
	def __init__(self, **kwargs):
		self._qlist = list()
		self.queryResult = list()

		keylist = ['site','title','url','filetype','link','kw']
		for key,value in kwargs.iteritems():
			if key not in keylist:
				self._qlist.append(["",'kw',value])
			self._qlist.append(["",key,value])


	def __neg__(self):
		self._qlist[0][0] = "-"
		return self

	def __pos__(self):
		self._qlist[0][0] = "+"
		return self

	def __or__(self, obj):
		self._qlist += obj._qlist
		return self


	def genKeyword(self, engine):
		'''
		Generate keyword string.
		'''
		config = SearchConfig(engine)
		keyword = ""
		for line in self._qlist:
			if line[1] in config['ghsyn']:
				if config['ghsyn'][line[1]]:
					keyword += line[0] + config['ghsyn'][line[1]] + ":" + line[2] + " "
				else:
					keyword += line[0] + line[2] + " "
			elif line[1] == "kw":
				keyword += line[0] + line[2] + " "

		return urllib.quote(keyword.strip())


	def doSearch(self, engine="baidu", size=500):
		'''
		Search in search engine.
		'''
		keyword = self.genKeyword(engine)
		if engine == "baidu":
			baidu = Baidu(size=size)
			return baidu.search(keyword)
		elif engine == "bing":
			bing = Bing(size=size)
			return bing.search(keyword)
		elif engine == "google":
			google = Google(size=size)
			return google.search(keyword)
		else:
			return None


class SearchEngine(object):
	'''
	Base searchengine class.
	input:
		size: specified the amount of the result
		engine: the engine name
	'''
	def __init__(self, engine, size=500):
		self.size = size
		self.retry = 20
		self.config = SearchConfig(engine)
		self.userAgents = UserAgents()

		self.url = self.config['url']
		defaultParam = genUrlParam(None, None, **self.config['default'])
		self.url += defaultParam

		#this signature string illustrate the searchengine find something, should be redefined in subclass
		self.findSignature = ""
		#this signature string illustrate the searchengine find nothing, should be redefined in subclass
		self.notFindSignature = ""


	def search(self, keyword, size=None):
		'''
		Use searchengine to search specified keyword.
		input:
			keyword: the keyword to search
			size: the length of search result
		'''
		size = size if size else self.size
		pageSize = self.config['param']['pgsize']['max']
		pages = size / pageSize

		keywordParam = genUrlParam(self.config['param']['query'], keyword)
		pageSizeParam = genUrlParam(self.config['param']['pgsize']['key'], pageSize)
		url = self.url + keywordParam + pageSizeParam

		result = list()
		for p in xrange(pages+1):
			pageNumParam = genUrlParam(self.config['param']['pgnum'], p*pageSize)
			tmpurl = url + pageNumParam

			result += self._search(tmpurl)

		self.queryResult = result
		return result


	def _search(self, url):
		'''
		Request with specified url, parse the reponse html document.
		input:
			url: the query url
		output:
			return the search result, result format is:
				[[titel,url,brief-information],[...]...]
		'''
		for i in xrange(self.retry):
			#use timeout and random user-agent to bypass IP restrict policy
			timeout = random.randint(1,3)
			time.sleep(timeout)

			userAgent = self.userAgents[random.randint(0,len(self.userAgents))-1]
			xforward = "192.168.3." + str(random.randint(1,255))

			headers = {"User-Agent":userAgent, "X-Forward-For":xforward, "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"}
			try:
				reponse = requests.get(url, headers=headers)
			except:
				continue

			print "debug",url
			print "debug",len(reponse.text)
			#print "debug",reponse.text

			if self.findSignature in reponse.text:
				break
			if self.notFindSignature in reponse.text:
				break

		return self._parseHtml(reponse.text)


	def _parseHtml(self, document):
		'''
		Parse html return the formated result. Should be redefine in subclass.
		input:
			the html document
		output:
			return the formated search result, result format is:
				[[titel,url,brief-information],[...]...]
		'''
		pass



class Baidu(SearchEngine):
	'''
	Baidu search engine.
	input:
		size: specified the amount of the result
	example:
		baidu=Baidu()
		baidu.search("site:xxx.com password.txt")
	'''
	def __init__(self, size=500):
		super(Baidu,self).__init__("baidu",size)
		self.findSignature = "class=f"
		self.notFindSignature = "noresult.html"


	def _parseHtml(self, document):
		result = list()

		document = BeautifulSoup(document)
		attrs={"class":"f"}
		relist = document.findAll("td", attrs=attrs)
		if not relist:
			return result

		for line in relist:
			title = "".join([x.string for x in line.a.font.contents])
			url = line.a["href"]
			briefDoc = line.a.nextSibling.nextSibling.contents
			brief = briefDoc[0].string + (briefDoc[1].string if briefDoc[1].string else "")
			result.append([title, url, brief])

		return result


class Bing(SearchEngine):
	'''
	Bing search engine.
	input:
		size: specified the amount of the result
	example:
		bing=Bing()
		bing.search("site:xxx.com password.txt")
	'''
	def __init__(self, size=500):
		super(Bing,self).__init__("bing",size)
		self.findSignature = 'class="b_algo"'
		self.notFindSignature = 'class="b_no"'

	def _parseHtml(self, document):
		result = list()

		document = BeautifulSoup(document)
		attrs = {"class":"b_algo"}
		relist = document.findAll("li", attrs=attrs)
		if not relist:
			return result

		for line in relist:
			title = "".join([x.string for x in line.h2.a.contents])
			url = line.h2.a["href"]
			brief = "".join([x.string for x in line.contents[1].p.contents])
			result.append([title, url, brief])

		return result

#text = '''
#<!DOCTYPE html><!--STATUS OK--><html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><title>百度搜索_site:huawei.com</title><style>body{margin:0}.f14{font-size:14px}.f10{font-family:"Arial";font-size:10.5pt}.c{color:#666}.p2{font-family:"Arial";line-height:120%;width:100%;align:left;margin-left:-12pt}.i0{font-size:12px;font-weight:bold;color:#000}.formfont{font-family:"Verdana","Arial","Helvetica","sans-serif";font-size:16px}td{font-size:9pt;line-height:18px}.t{color:#fff;font-weight:bold;text-decoration:none}a.t:hover{text-decoration:underline}table{white-space:normal;line-height:normal;font-weight:normal;font-size:medium;font-variant:normal;font-style:normal;color:-webkit-text;text-align:start}</style><script language="javascript">function h(obj,url){obj.style.behavior='url(#default#homepage)';obj.setHomePage(url);}if (window.name == 'nw') { window.name = '';}function ga(o,e){if (document.getElementById){a=o.id.substring(1); p = "";r = "";g = e.target;if (g) { t = g.id;f = g.parentNode;if (f) {p = f.id;h = f.parentNode;if (h) r = h.id;}} else{h = e.srcElement;f = h.parentNode;if (f) p = f.id;t = h.id;}if (t==a || p==a || r==a) return true;window.open(document.getElementById(a).href,'_blank')}}function mysubmit(form){form.q.value=form.wd.value;form.wd.value="site:www.baidu.com"+" "+form.wd.value;form.action="/s";form.submit();return true;}</script></head><body bgcolor=#ffffff text=#000000 link=#261CDC alink=#261CDC vlink=#261CDC><table width=100% border=0><form name=f1 action="/s"><tr valign=middle height=55><td width=260><a href="http://www.baidu.com/"><img src="http://s1.bdstatic.com/r/www/cache/mid/static/global/img/logo-yy_745b0a04.gif" border="0"></a></td><td><a onClick="h(this,'http://www.baidu.com')" href="#" class="c">设百度为首页</a>&nbsp;<a href="http://www.baidu.com/gaoji/advanced.html" class=c>高级搜索</a>&nbsp;<a href=http://www.baidu.com/search/jiqiao.html target="_blank" class="c">帮助</a>&nbsp;<br><input type=hidden name=q><input type=hidden name=tn value="baidulocal"><input type=hidden name=ct value="2097152"><input type=hidden name=si value=""><input type=hidden name=ie value="utf-8"><input type=hidden name=bs value="site:huawei.com"><input type=hidden name=cl value=3><input name=wd size=30 class=formfont value="site:huawei.com">&nbsp;<input type=submit value=百度站内搜索></td></tr></form></table><table bgColor=#e6e6e6 border=0 cellPadding=0 cellSpacing=0 width=100%><tr><td width=12></td><td height=18>百度为您找到相关网页760篇。</td></tr><tr><td colspan=2 bgColor=#999999 height=2></td></tr></table><br clear=all><table width=100% border=0><tr><td><ol><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://xinsheng.huawei.com/" target="_blank"><font size="3">心声社区</font></a><br><font size=-1>·心声年度盘点第一波||再见,2014。你好,2...·一张图看懂首届为爱奔跑捐了多少钱·华为大学搬迁松山湖,版主穿越未来看培训·摄影真的很简单,ToNy带你看世界·...<br><font color=#008000>xinsheng.huawei.com/&nbsp;89K&nbsp;2015-10-9&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105c8c3a580ed73f69c0d0622593c00dc43f4c413037bee43a365559939373&p=92769a47879501ed0ebd9b7d0d158a&newp=c077c25486cc42af5bb7c7710f4097231610db2151d4d61625&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://club.huawei.com/" target="_blank"><font size="3">花粉俱乐部</font></a><br><font size=-1>Zero手环已经发售一段时间,好多花粉都已经成功拿到了心爱的手环,大家对于这款高颜值的手环也是十分满意,同时也献上了“Zero”的时尚大片,还有和自己的合影~注意,Zer...<br><font color=#008000>club.huawei.com/&nbsp;65K&nbsp;2015-10-14&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104789214943801466908350288f8448e435061e5a72a6e667741f&p=8b2a9715d9c241e703f3d4655054&newp=80759a44d69b17ed1aacc7710f5f92695c16ed623c8f86573d95&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://www.huawei.com/" target="_blank"><font size="3">华为- 更美好的全联接世界</font></a><br><font size=-1>产品支持 软件下载 案例库 华为培训 华为认证 工具 技术论坛  运营商用户 产品支持 Group Space 公告 华为资料直通车 培训 HedEx Lite 知道社区  在线技术支持、软...<br><font color=#008000>www.huawei.com/&nbsp;125K&nbsp;2015-10-15&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f7397b84954224c3933fc239045c5323befb712d&p=9d72ce16d9c111a05fe9d335545d&newp=882a92418dd012a05afbc623455192695c16ed64388cc3&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://e-learning.huawei.com/" target="_blank"><font size="3">华为培训服务</font></a><br><font size=-1>华为业务发展学习解决方案基于华为成功实践和电信运营管理标准,为客户提供CEM &amp; SQI能力发展学习解决方案和网络运维能力提升学习解决方案,助力运营商业务目标达成。  ...<br><font color=#008000>e-learning.huawei.com/&nbsp;111K&nbsp;2015-9-29&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece7631041c0666f0ad7307c8b8b492ac3933fc9230804103df4bb50734d5bced1393a41f946&p=8b2a9715d9c446e703f3d4655054&newp=80759a42d19b17ed1aacc7710f5f92695c16ed643b8f86573d95&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://weblink.huawei.com/" target="_blank"><font size="3">Welcome to Huawei Web Systems - 欢迎光临华为Web系统</font></a><br><font size=-1>EPMS Engineering Project Management 工程项目管理系统 PSDS Parts Service Delivery System 备件服务交付系统 Train-MIS Training Management 培训管理系统 TSWS Work ...<br><font color=#008000>weblink.huawei.com/&nbsp;5K&nbsp;2007-5-19&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece76310538036470fdc3a2bd7a74f3887d61fc8735b36163bbca633674d4485ca&p=9f759a46d6c509ec0be29668495189&newp=aa7bc64ad4d05fe012bd9b7d0d109d231610db2151d4d0136ccadc02&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://hwtrip.huawei.com/" target="_blank"><font size="3">华为爱旅-邮轮旅游,出境旅游,海岛旅游,景点门票,周边旅游</font></a><br><font size=-1>歌诗达邮轮 丽星邮轮 皇家加勒比邮轮 地中海邮轮 公主邮轮 其他  出境游 欧洲 韩国 澳大利亚 美国 泰国 日本 新加坡  港澳台 香港 澳门 台湾  欧洲 德国 法国 ...<br><font color=#008000>hwtrip.huawei.com/&nbsp;127K&nbsp;2015-10-8&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104c9220590fc2743ca08a522c91c41384642c101a39feaf627f5052dc&p=9f759a46d6c509ec0be29668495189&newp=aa7bc64ad4d05fe012bd9b7d0d109d231610db2151d0d606619bd9&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://www.huawei.com/us/index.htm" target="_blank"><font size="3">Huawei United States - A leading global ICT solutions provider</font></a><br><font size=-1>We provide comprehensive support for your business growth, including online assistance, document sharing, and more. ABOUT US  Corporate Information Connected Po...<br><font color=#008000>www.huawei.com/us/ind...htm&nbsp;57K&nbsp;2015-8-24&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f7397b84954224c3933fc239045c0027fee07b74474ec4c50b3d47f05d19b7b0607d&p=92769a47879501ed0ebd9b7d0d168a&newp=c077c25486cc42af58b7c7710f4097231610db2151d4d71525&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://career.huawei.com/" target="_blank"><font size="3">华为招聘</font></a><br><font size=-1>招聘维信公众号  扫我关注Huawei Copyright ©2015版权所有...<br><font color=#008000>career.huawei.com/&nbsp;4K&nbsp;2015-9-18&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104784264e03c0743ca08a522c91c41384642c101a39feaf627f5052dc&p=9d72ce16d9c111a05bed9639464f9c&newp=882a9645d49852fc57ef822c505e90231610db2151d4d51024c7&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://support.huawei.com/" target="_blank"><font size="3">技术支持 - 欢迎访问华为公司网站</font></a><br><font size=-1>提示 确定 您使用的浏览器不支持自动加入收藏夹,请使用Ctrl+D进行添加 长时间未操作或已退出登录,请重新登录 ...<br><font color=#008000>support.huawei.com/&nbsp;55K&nbsp;2015-10-14&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105790245b09c0252bd7a74f3887d61fc8735b36163bbca633674d4485ca&p=8b2a9715d9c745e703f3d4655054&newp=80759a41d29b17ed1aacc7710f5f92695c16ed67388f86573d95&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://developer.huawei.com/" target="_blank"><font size="3">华为开发者联盟</font></a><br><font size=-1>·前方高能预警:一大波价值3000元的开发者大会门票向你袭来! 2015-10-13  ·第三期启蒙计划推荐应用公示! 2015-10-08  ·期待已久的第二期启蒙计划推荐应用公示...<br><font color=#008000>developer.huawei.com/&nbsp;125K&nbsp;2015-10-15&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104080224e0add216b97c715088ed41bd63300564711b2e6783f04418e852a68&p=8b2a9715d9c741e703f3d4655054&newp=80759a41d69b17ed1aacc7710f5f92695c16ed673c8f86573d95&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br></ol><ol>1&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=10&tn=baidulocal&ie=utf-8">[2]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=20&tn=baidulocal&ie=utf-8">[3]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=30&tn=baidulocal&ie=utf-8">[4]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=40&tn=baidulocal&ie=utf-8">[5]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=50&tn=baidulocal&ie=utf-8">[6]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=60&tn=baidulocal&ie=utf-8">[7]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=70&tn=baidulocal&ie=utf-8">[8]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=80&tn=baidulocal&ie=utf-8">[9]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=90&tn=baidulocal&ie=utf-8">[10]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=10&tn=baidulocal&ie=utf-8"><font size=3>下一页</font></a>&nbsp;</ol></td></tr></table><div style="text-align:center;background-color:#e6e6e6;height:20px;padding-top:2px;font-size:12px;"><a href="http://www.baidu.com/duty/copyright.html" class="c">&copy;2015</a>&nbsp;Baidu&nbsp;<a href="http://www.baidu.com/duty/index.html" class="c">免责声明</a>&nbsp;<font color=#666666>此内容系百度根据您的指令自动搜索的结果，不代表百度赞成被搜索网站的内容或立场</font></div></body></html>
#'''#

#text2 = '''
#<!DOCTYPE html><!--STATUS OK--><html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><title>百度搜索_intitle:huawei.com</title><style>body{margin:0}.f14{font-size:14px}.f10{font-family:"Arial";font-size:10.5pt}.c{color:#666}.p2{font-family:"Arial";line-height:120%;width:100%;align:left;margin-left:-12pt}.i0{font-size:12px;font-weight:bold;color:#000}.formfont{font-family:"Verdana","Arial","Helvetica","sans-serif";font-size:16px}td{font-size:9pt;line-height:18px}.t{color:#fff;font-weight:bold;text-decoration:none}a.t:hover{text-decoration:underline}table{white-space:normal;line-height:normal;font-weight:normal;font-size:medium;font-variant:normal;font-style:normal;color:-webkit-text;text-align:start}</style><script language="javascript">function h(obj,url){obj.style.behavior='url(#default#homepage)';obj.setHomePage(url);}if (window.name == 'nw') { window.name = '';}function ga(o,e){if (document.getElementById){a=o.id.substring(1); p = "";r = "";g = e.target;if (g) { t = g.id;f = g.parentNode;if (f) {p = f.id;h = f.parentNode;if (h) r = h.id;}} else{h = e.srcElement;f = h.parentNode;if (f) p = f.id;t = h.id;}if (t==a || p==a || r==a) return true;window.open(document.getElementById(a).href,'_blank')}}function mysubmit(form){form.q.value=form.wd.value;form.wd.value="site:www.baidu.com"+" "+form.wd.value;form.action="/s";form.submit();return true;}</script></head><body bgcolor=#ffffff text=#000000 link=#261CDC alink=#261CDC vlink=#261CDC><table width=100% border=0><form name=f1 action="/s"><tr valign=middle height=55><td width=260><a href="http://www.baidu.com/"><img src="http://s1.bdstatic.com/r/www/cache/mid/static/global/img/logo-yy_745b0a04.gif" border="0"></a></td><td><a onClick="h(this,'http://www.baidu.com')" href="#" class="c">设百度为首页</a>&nbsp;<a href="http://www.baidu.com/gaoji/advanced.html" class=c>高级搜索</a>&nbsp;<a href=http://www.baidu.com/search/jiqiao.html target="_blank" class="c">帮助</a>&nbsp;<br><input type=hidden name=q><input type=hidden name=tn value="baidulocal"><input type=hidden name=ct value="2097152"><input type=hidden name=si value=""><input type=hidden name=ie value="utf-8"><input type=hidden name=bs value="intitle:huawei.com"><input type=hidden name=cl value=3><input name=wd size=30 class=formfont value="intitle:huawei.com">&nbsp;<input type=submit value=百度站内搜索></td></tr></form></table><table bgColor=#e6e6e6 border=0 cellPadding=0 cellSpacing=0 width=100%><tr><td width=12></td><td height=18>百度为您找到相关网页760篇。</td></tr><tr><td colspan=2 bgColor=#999999 height=2></td></tr></table><br clear=all><table width=100% border=0><tr><td><ol><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://www.huawei.com/" target="_blank"><font size="3"><font color="#c60a00">华为</font>- 更美好的全联接世界</font></a><br><font size=-1><font color="#c60a00">华为</font>是全球领先的信息与通信解决方案供应商。我们围绕客户的需求持续创新,与合作伙伴开放合作,在电信网络、终端和云计算等领域构筑了端到端的解决方案优势。我们致力...<br><font color=#008000>www.huawei.com/&nbsp;125K&nbsp;2015-10-15&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f7397b84954224c3933fc239045c5323befb712d4a4380802b3c16ae394bea87217347527de8&p=882a9241c08652f84ebe9b7c4f48&newp=8f769a479d934ea85cb5c3645b5492695c16ed64389c&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://support.huawei.com/" target="_blank"><font size="3">技术支持 - 欢迎访问<font color="#c60a00">华为</font>公司网站</font></a><br><font size=-1>中低端防火墙 提示 确定 您使用的浏览器不支持自动加入收藏夹,请使用Ctrl+D进行添加 长时间未操作或已退出登录,请重新登录 ...<br><font color=#008000>support.huawei.com/&nbsp;38K&nbsp;2015-10-9&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105790245b09c0252bd7a74f3887d61fc8735b36163bbca633674d4485ca262052ea1e07fdf14665377437b6eb99d515&p=8d6dc64ad48957ff57ee94795b4093&newp=9b678d16d9c111a05bed932f514bbb231610db2151d4d612&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://www.vmall.com/" target="_blank"><font size="3">为了您的帐号安全,<font color="#c60a00">华为</font>商城强烈建议您进行手机帐号的绑定;绑定后,...</font></a><br><font size=-1><font color="#c60a00">华为</font>商城是<font color="#c60a00">华为</font>旗下面向全国服务的电子商务平台官网,我们提供正品<font color="#c60a00">华为</font>手机(<font color="#c60a00">华为</font>MateS、<font color="#c60a00">华为</font>P8、荣耀6Plus、荣耀畅玩4C、<font color="#c60a00">华为</font>Mate7、荣耀X2、荣耀畅玩4X、荣耀3C畅玩...<br><font color=#008000>www.vmall.com/&nbsp;114K&nbsp;2015-10-14&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f72763848e4b68d4e419ce3b4655023ba3ed287857579692277000df5e5c9de73702665e7f&p=847ccf1f85cc43ff57ee947b59418d&newp=c36ed416d9c105e442bd9b7d0d1386231610db2151ddd55134ce&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://emui.huawei.com/" target="_blank"><font size="3"><font color="#c60a00">huawei</font> emui</font></a><br><font size=-1>花粉俱乐部是<font color="#c60a00">华为</font>官方唯一的以服务花粉为宗旨的综合性网站,提供最新<font color="#c60a00">华为</font>手机产品资讯、最丰富的应用软件主题游戏EMUI ROM资源、最丰富的花粉活动信息,汇集<font color="#c60a00">华为</font>手机、...<br><font color=#008000>emui.huawei.com/&nbsp;19K&nbsp;2015-10-12&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104188214243801466908350288f8448e435061e5a72a6e667741f5e949639305ab8482cfdf04165367371eac4&p=9b769a478b934eac58e9d460584f8f&newp=973ecf16d9c107e618bd9b7d0d1298231610db2151d4d4533694&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://club.huawei.com/" target="_blank"><font size="3">花粉俱乐部</font></a><br><font size=-1>花粉俱乐部是<font color="#c60a00">华为</font>官方唯一的以服务花粉为宗旨的综合性网站,提供最新<font color="#c60a00">华为</font>手机产品资讯、最丰富的应用软件主题游戏EMUI ROM资源、最丰富的花粉活动信息,汇集<font color="#c60a00">华为</font>手机、...<br><font color=#008000>club.huawei.com/&nbsp;68K&nbsp;2015-10-1&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104789214943801466908350288f8448e435061e5a72a6e667741f5e949639305ab8482cfdf04165367371eac4&p=b4759a46d6c301b50be29664534f96&newp=882a9645d69102e034b9c7710f548b231610db2151d4d0152d97dc24c7&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://y.liuxue86.com/details/11970" target="_blank"><font size="3">【<font color="#c60a00">华为</font>官方网站】<font color="#c60a00">华为</font>官方网站网址:http://www.<font color="#c60a00">huawei.com</font>/|华为...</font></a><br><font size=-1>网站简介: <font color="#c60a00">华为</font>是全球领先的电信解决方案供应商,1988年成立于中国深圳,为世界各地通信运营商及网络拥有者提供硬件、软件、解决方案和服务。公司在电信基础网络、业务与...<br><font color=#008000>y.liuxue86.com/details/11...&nbsp;21K&nbsp;2015-10-13&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105dc0666e0adb247690871f7bc3933fc239045c1131a5e87c7c5119d0c6776203bb0c01aaa63928705065e0c0df893acabbe53f2ef876692f&p=b4759a46d6c601b50be29664534f96&newp=882a9645d39102e034b9c7710f548b231610db2151d2d5473c9bff1c&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://developer.huawei.com/" target="_blank"><font size="3"><font color="#c60a00">华为</font>开发者联盟</font></a><br><font size=-1><font color="#c60a00">华为</font>开发者联盟旨在整合及协调产业链资源,为联盟成员提供业务发展的机会和资源,提升联盟成员在安卓平台上的移动互联网领域的合作创新能力,实现商业价值。促进移动互联网...<br><font color=#008000>developer.huawei.com/&nbsp;127K&nbsp;2015-10-9&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9d78d513d99906fc1dbacf690c66c0666e4381136d8a8f013894cd47c9221d03506790a63a744740849b212556ef5e5c9daa712172547ba09bbfd91782a6&p=80678315d9c041aa1ffbca2d021489&newp=9a71da0386cc42af5dfe8e2d0214c6231610db2151d4d6106cce&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://consumer.huawei.com/cn/contact-us/" target="_blank"><font size="3">联系我们-<font color="#c60a00">华为</font>消费者业务邮箱:worksmart@<font color="#c60a00">huawei.com</font>进入华为byod移</font></a><br><font size=-1>为您提供在线服务,远程服务,邮件,电话等多种支持方式。请从列表中联系方式和我们取得联系。<br><font color=#008000>consumer.huawei.com/cn/contact-...&nbsp;96K&nbsp;2015-8-30&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9d78d513d99906fc1dbacf690c66c0666e4381136d8a8f013894cd47c9221d03506790a63a734d589282233041b8492bb0b76537605837b7ec99d515c0eace357ed57b72234dc05612a55eeed6&p=c078d416d9c111a05bed942c59649f&newp=8f3bc54ad5c341e517a7cc2d0214c6231610db2151dcd05f309ecb&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://weblink.huawei.com/" target="_blank"><font size="3">Welcome to <font color="#c60a00">Huawei</font> Web Systems - 欢迎光临<font color="#c60a00">华为</font>Web系统</font></a><br><font size=-1><font color="#c60a00">Huawei</font> Web Systems - <font color="#c60a00">华为</font>Web系统  Internet  SUPPORT Technical Support 技术支持网站 GCRMS Overseas Call Center 海外客户问题管理系统EPMS...<br><font color=#008000>weblink.huawei.com/&nbsp;5K&nbsp;2007-5-19&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece76310538036470fdc3a2bd7a74f3887d61fc8735b36163bbca633674d4485ca262052ea1e07fdf14665377437b6eb99d515&p=882a9645d0d504bc0ffbc7710f5489&newp=8f769a479d934eac58ebcc29174095231610db2151d4d01334&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://lic.huawei.com/" target="_blank"><font size="3">lic.<font color="#c60a00">huawei.com</font>/</font></a><br><font size=-1>(2)内网: http://w3.<font color="#c60a00">huawei.com</font>/sdp (华为员工通过W3帐号访问) 二、其他说明: 由于两个发放平台的帐号登录方式不一致,因此原系统外部用户需要重新注册申请...<br><font color=#008000>lic.huawei.com/&nbsp;21K&nbsp;2014-5-23&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece76310488c370e54f7397b84954224c3933fc239045c5323befb712d4a4380802b3c16ae394bea87217347527de8&p=836dc90fc8904ead08e2977e080086&newp=836ac64ad4db11a05bed91381642a5231610db2151d4d21267&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br></ol><ol>1&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=10&tn=baidulocal&ie=utf-8">[2]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=20&tn=baidulocal&ie=utf-8">[3]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=30&tn=baidulocal&ie=utf-8">[4]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=40&tn=baidulocal&ie=utf-8">[5]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=50&tn=baidulocal&ie=utf-8">[6]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=60&tn=baidulocal&ie=utf-8">[7]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=70&tn=baidulocal&ie=utf-8">[8]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=80&tn=baidulocal&ie=utf-8">[9]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=90&tn=baidulocal&ie=utf-8">[10]</a>&nbsp;<a href="s?wd=intitle%3Ahuawei.com&pn=10&tn=baidulocal&ie=utf-8"><font size=3>下一页</font></a>&nbsp;</ol></td></tr></table><div style="text-align:center;background-color:#e6e6e6;height:20px;padding-top:2px;font-size:12px;"><a href="http://www.baidu.com/duty/copyright.html" class="c">&copy;2015</a>&nbsp;Baidu&nbsp;<a href="http://www.baidu.com/duty/index.html" class="c">免责声明</a>&nbsp;<font color=#666666>此内容系百度根据您的指令自动搜索的结果，不代表百度赞成被搜索网站的内容或立场</font></div></body></html>
#'''

#document = BeautifulSoup(text)
#attrs={"class":"f"}
#relist = document.findAll("td", attrs=attrs)
#re = relist[0]
##print type(re.a.font), re.a.font
#document2 = BeautifulSoup(text2)
#relist2 = document2.findAll("td", attrs=attrs)
#re2 = relist2[0]

#['site','title','url','filetype','link','kw']

#query = Query(filetype="xls") | Query(site="huawei.com")
#query = Query(title="torrent")
query = Query(filetype="xls")
#print query.genKeyword("bing")
#query = Query(kw="siw")
re = query.doSearch(engine="bing", size=5)
#print re
for line in re:
	print line[0]
	print line[1]
	print line[2]

