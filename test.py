#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import os
import random
import time

import requests
import yaml
from thirdparty.BeautifulSoup import BeautifulSoup


class SearchConfig(object):
	def __new__(cls, engine):
		configFile = os.path.join("plugin","config","searchengine.yaml")
		try:
			with open(configFile, "r") as fd:
				config = yaml.load(fd)[engine]
		except IOError:
			print "read configfile error"
			return None
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
			userAgents = [v for k,v in config]


def genUrlParam(key, value, **kwargs):
	if kwargs:
		return "&".join([k+"="+v for k,v in kwargs.iteritems()]) + "&"
	else:
		return key + "=" + str(value) + "&"


class Query(object):
	'''
	Build query keyword
	parameter:
		site: seach specified site
		title: search in title
		url: search in url
		filetype: search files with specified file type
		ext: search files with specified extetion
		link: search in link
		kw: raw keywords to search 
	example:
		query = Query(site="xxx.com") | -Query(site="www.xxx.com") | Query(kw="password")
		query.doSearch(engine="baidu")
	'''
	def __init__(self, **kwargs):
		self._qlist = list()
		self.queryResult = list()

		for key,value in kwargs.iteritems():
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
		config = SearchConfig("baidu")
		keyword = ""
		for line in self._qlsit:
			if line[1] in config['ghsyn']:
				line[1] = config['ghsyn'][line[1]]
				keyword += "".join(line)+" "
				continue
			elif line[1] == "kw":
				keyword += line[0]+line[2]

		return keyword


	def doSearch(engine="baidu", size=500, encode="utf-8"):
		keyword = self.genKeyword(engine)
		if engine == "baidu":
			baidu = Baidu(size=size, encode=encode)
			return baidu.search(keyword)
		else:
			return None


class Baidu(object):
	'''
	Baidu search engine.
	parameter:
		size: specified the amount of the result
		encode: specified the url encode method
	example:
		baidu=Baidu()
		baidu.search("site:xxx.com password.txt")
	'''
	def __init__(self, size=500, encode="utf-8"):
		self.size = size
		self.encode = encode

		self.config = SearchConfig("baidu")
		self.userAgents = UserAgents()

		self.url = self.config['url']

		defaultParam = genUrlParam(None, None, **config['default'])
		self.url += defaultParam

		encodeParam = genUrlParam(self.config['param']['encode'], encode)
		self.url += encodeParam


	def search(self, keyword, size=None):
		'''
		Use baidu to search specified keyword.
		parameter:
			keyword: the keyword to search
			size: the length of search result
		'''
		size = size if size else self.size
		pageSize = self.config['param']['pgsize']['max']
		pages = size / pageSize

		keywordParam = genUrlParam(self.config['param']['query'], keyword)
		pageSizeParam = genUrlParam(self.config['param']['pgsize']['key'], keyword)

		url += keywordParam + pageSizeParam

		result = list()
		for p in xrange(pages+1):
			pageNumParam = genUrlParam(self.config['param']['pgnum'], p*pageSize)
			tmpurl = url + pageNumParam

			result.append(self._search(tmpurl))

		self.queryResult = result
		return result


	def _search(self, url):
		'''
		Request with specified url, parse the reponse html document.
		parameter:
			url: the query url
		return:
			return the search result, result format is:
				[[titel,url,brief-information],[...]...]
		'''
		result = list()
		#use timeout and random user-agent to bypass baidu IP restrict policy
		timeout = random.randint(1,3)
		time.sleep(timeout)

		headers = {"User-Agent": self.userAgents[random.randint(0,len(self.userAgents))]}
		reponse = requests.get(url, headers=headers)
		# 判断是否返回了结果
		document = BeautifulSoup(reponse.text)

		attrs={"class":"f"}
		relist = doc.findAll("td", attrs=attrs)

		for line in relist:
			title = line.font.string
			url = line.a["href"]
			brief = line.a.nextSibling.nextSibling.contents[0]
			result.append([title, url, brief])



text = u'''
<!DOCTYPE html><!--STATUS OK--><html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><title>百度搜索_site:huawei.com</title><style>body{margin:0}.f14{font-size:14px}.f10{font-family:"Arial";font-size:10.5pt}.c{color:#666}.p2{font-family:"Arial";line-height:120%;width:100%;align:left;margin-left:-12pt}.i0{font-size:12px;font-weight:bold;color:#000}.formfont{font-family:"Verdana","Arial","Helvetica","sans-serif";font-size:16px}td{font-size:9pt;line-height:18px}.t{color:#fff;font-weight:bold;text-decoration:none}a.t:hover{text-decoration:underline}table{white-space:normal;line-height:normal;font-weight:normal;font-size:medium;font-variant:normal;font-style:normal;color:-webkit-text;text-align:start}</style><script language="javascript">function h(obj,url){obj.style.behavior='url(#default#homepage)';obj.setHomePage(url);}if (window.name == 'nw') { window.name = '';}function ga(o,e){if (document.getElementById){a=o.id.substring(1); p = "";r = "";g = e.target;if (g) { t = g.id;f = g.parentNode;if (f) {p = f.id;h = f.parentNode;if (h) r = h.id;}} else{h = e.srcElement;f = h.parentNode;if (f) p = f.id;t = h.id;}if (t==a || p==a || r==a) return true;window.open(document.getElementById(a).href,'_blank')}}function mysubmit(form){form.q.value=form.wd.value;form.wd.value="site:www.baidu.com"+" "+form.wd.value;form.action="/s";form.submit();return true;}</script></head><body bgcolor=#ffffff text=#000000 link=#261CDC alink=#261CDC vlink=#261CDC><table width=100% border=0><form name=f1 action="/s"><tr valign=middle height=55><td width=260><a href="http://www.baidu.com/"><img src="http://s1.bdstatic.com/r/www/cache/mid/static/global/img/logo-yy_745b0a04.gif" border="0"></a></td><td><a onClick="h(this,'http://www.baidu.com')" href="#" class="c">设百度为首页</a>&nbsp;<a href="http://www.baidu.com/gaoji/advanced.html" class=c>高级搜索</a>&nbsp;<a href=http://www.baidu.com/search/jiqiao.html target="_blank" class="c">帮助</a>&nbsp;<br><input type=hidden name=q><input type=hidden name=tn value="baidulocal"><input type=hidden name=ct value="2097152"><input type=hidden name=si value=""><input type=hidden name=ie value="utf-8"><input type=hidden name=bs value="site:huawei.com"><input type=hidden name=cl value=3><input name=wd size=30 class=formfont value="site:huawei.com">&nbsp;<input type=submit value=百度站内搜索></td></tr></form></table><table bgColor=#e6e6e6 border=0 cellPadding=0 cellSpacing=0 width=100%><tr><td width=12></td><td height=18>百度为您找到相关网页760篇。</td></tr><tr><td colspan=2 bgColor=#999999 height=2></td></tr></table><br clear=all><table width=100% border=0><tr><td><ol><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://xinsheng.huawei.com/" target="_blank"><font size="3">心声社区</font></a><br><font size=-1>·心声年度盘点第一波||再见,2014。你好,2...·一张图看懂首届为爱奔跑捐了多少钱·华为大学搬迁松山湖,版主穿越未来看培训·摄影真的很简单,ToNy带你看世界·...<br><font color=#008000>xinsheng.huawei.com/&nbsp;89K&nbsp;2015-10-9&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105c8c3a580ed73f69c0d0622593c00dc43f4c413037bee43a365559939373&p=9f769a479e8b13ff57ee947d587a93&newp=8b2a97118d8411a05bed972a134e94231610db2151d4d6162b8fd4&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://club.huawei.com/" target="_blank"><font size="3">花粉俱乐部</font></a><br><font size=-1>Zero手环已经发售一段时间,好多花粉都已经成功拿到了心爱的手环,大家对于这款高颜值的手环也是十分满意,同时也献上了“Zero”的时尚大片,还有和自己的合影~注意,Zer...<br><font color=#008000>club.huawei.com/&nbsp;65K&nbsp;2015-10-14&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104789214943801466908350288f8448e435061e5a72a6e667741f&p=9f769a479e8b13ff57ec942b6152&newp=8b2a97118d8411a059edc060555592695c16ed623c838b52&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://www.huawei.com/" target="_blank"><font size="3">华为- 更美好的全联接世界</font></a><br><font size=-1>产品支持 软件下载 案例库 华为培训 华为认证 工具 技术论坛  运营商用户 产品支持 Group Space 公告 华为资料直通车 培训 HedEx Lite 知道社区  在线技术支持、软...<br><font color=#008000>www.huawei.com/&nbsp;127K&nbsp;2015-9-28&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f7397b84954224c3933fc239045c5323befb712d&p=9f769a479e8b13ff57ee947a587a93&newp=8b2a97118d8411a05bed902a134e94231610db2151d3844e38&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://e-learning.huawei.com/" target="_blank"><font size="3">华为培训服务</font></a><br><font size=-1>华为业务发展学习解决方案基于华为成功实践和电信运营管理标准,为客户提供CEM &amp; SQI能力发展学习解决方案和网络运维能力提升学习解决方案,助力运营商业务目标达成。  ...<br><font color=#008000>e-learning.huawei.com/&nbsp;111K&nbsp;2015-9-29&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece7631041c0666f0ad7307c8b8b492ac3933fc9230804103df4bb50734d5bced1393a41f946&p=9f769a479e8b13ff57ea932b6152&newp=8b2a97118d8411a05feac060555592695c16ed643b838b52&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://weblink.huawei.com/" target="_blank"><font size="3">Welcome to Huawei Web Systems - 欢迎光临华为Web系统</font></a><br><font size=-1>EPMS Engineering Project Management 工程项目管理系统 PSDS Parts Service Delivery System 备件服务交付系统 Train-MIS Training Management 培训管理系统 TSWS Work ...<br><font color=#008000>weblink.huawei.com/&nbsp;5K&nbsp;2007-5-19&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece76310538036470fdc3a2bd7a74f3887d61fc8735b36163bbca633674d4485ca&p=9f769a479e8b13ff57ee9478587a93&newp=8b2a97118d8411a05bed922a134e94231610db2151d4d0132b8fd4&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://www.huawei.com/us/index.htm" target="_blank"><font size="3">Huawei United States - A leading global ICT solutions provider</font></a><br><font size=-1>We provide comprehensive support for your business growth, including online assistance, document sharing, and more. ABOUT US  Corporate Information Connected Po...<br><font color=#008000>www.huawei.com/us/ind...htm&nbsp;57K&nbsp;2015-8-24&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f7397b84954224c3933fc239045c0027fee07b74474ec4c50b3d47f05d19b7b0607d&p=9f769a479e8b13ff57ee947e587a93&newp=8b2a97118d8411a05bed942a134e94231610db2151d4d7152b8fd4&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://hwtrip.huawei.com/" target="_blank"><font size="3">华为爱旅-邮轮旅游,出境旅游,海岛旅游,景点门票,周边旅游</font></a><br><font size=-1>歌诗达邮轮 丽星邮轮 皇家加勒比邮轮 地中海邮轮 公主邮轮 其他  出境游 欧洲 韩国 澳大利亚 美国 泰国 日本 新加坡  港澳台 香港 澳门 台湾  欧洲 德国 法国 ...<br><font color=#008000>hwtrip.huawei.com/&nbsp;127K&nbsp;2015-9-25&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104c9220590fc2743ca08a522c91c41384642c101a39feaf627f5052dc&p=9f769a479e8b13ff57ee947a587a93&newp=8b2a97118d8411a05bed902a134e94231610db2151d6d4412493&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://career.huawei.com/" target="_blank"><font size="3">华为招聘</font></a><br><font size=-1>招聘维信公众号  扫我关注Huawei Copyright ©2015版权所有...<br><font color=#008000>career.huawei.com/&nbsp;4K&nbsp;2015-9-18&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9d78d513d9d706ef06e2ce384b54c0676a499d326f9787423fc3933fc9230804103df4bb50734d5bce&p=882a9645d4b15ae449b5d02d0214c1&newp=882a9645d4811bc346be9b7c460885231610db2151d4d5103d8eff56&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://support.huawei.com/" target="_blank"><font size="3">技术支持 - 欢迎访问华为公司网站</font></a><br><font size=-1>提示 确定 您使用的浏览器不支持自动加入收藏夹,请使用Ctrl+D进行添加 长时间未操作或已退出登录,请重新登录 ...<br><font color=#008000>support.huawei.com/&nbsp;55K&nbsp;2015-10-13&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9d78d513d9d706ef06e2ce384b54c0676a499d227b9592483f928448e43e1c120231b8ac275541598cd8&p=882a9141a4d80abe00a9c7710f00&newp=882a914194992db10be29635134492695c16ed6738958a7961&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br><table border="0" cellpadding="0" cellspacing="0"><tr><td class=f><a href="http://developer.huawei.com/" target="_blank"><font size="3">华为开发者联盟</font></a><br><font size=-1>·前方高能预警:一大波价值3000元的开发者大会门票向你袭来! 2015-10-13  ·第三期启蒙计划推荐应用公示! 2015-10-08  ·期待已久的第二期启蒙计划推荐应用公示...<br><font color=#008000>developer.huawei.com/&nbsp;125K&nbsp;2015-10-14&nbsp;</font>-&nbsp;<a href="http://cache.baidu.com/c?m=9d78d513d9d706ef06e2ce384b54c0676a499d356b93874b2296c40884642c1b0035a6ec7c3510738298237a&p=882a9145a4d80abe00a9c7710f00&newp=882a914594992db10be29635134492695c16ed673c958a7961&user=baidu" target="_blank" class=m>百度快照</a><br></font></td></tr></table><br></ol><ol>1&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=10&tn=baidulocal&ie=utf-8">[2]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=20&tn=baidulocal&ie=utf-8">[3]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=30&tn=baidulocal&ie=utf-8">[4]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=40&tn=baidulocal&ie=utf-8">[5]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=50&tn=baidulocal&ie=utf-8">[6]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=60&tn=baidulocal&ie=utf-8">[7]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=70&tn=baidulocal&ie=utf-8">[8]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=80&tn=baidulocal&ie=utf-8">[9]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=90&tn=baidulocal&ie=utf-8">[10]</a>&nbsp;<a href="s?wd=site%3Ahuawei.com&pn=10&tn=baidulocal&ie=utf-8"><font size=3>下一页</font></a>&nbsp;</ol></td></tr></table><div style="text-align:center;background-color:#e6e6e6;height:20px;padding-top:2px;font-size:12px;"><a href="http://www.baidu.com/duty/copyright.html" class="c">&copy;2015</a>&nbsp;Baidu&nbsp;<a href="http://www.baidu.com/duty/index.html" class="c">免责声明</a>&nbsp;<font color=#666666>此内容系百度根据您的指令自动搜索的结果，不代表百度赞成被搜索网站的内容或立场</font></div></body></html>
'''

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

url = "http://www.baidu.com/s?wd=site%3Ahuawei.com&tn=baidulocal"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0"}

#re = requests.get(url, headers=headers)

#print re.text

doc = BeautifulSoup(text)
#print doc.prettify()
#print doc.findAll("table", border="0")
#print doc.head.title
re = list()
attrs={"class":"f"}
#relist = doc.findAll("td", attrs={"class","f"})
relist = doc.findAll("td", attrs=attrs)

for line in relist:
	title = line.font.string
	url = line.a["href"]
	brief = line.a.nextSibling.nextSibling.contents[0]
	re.append([title, url, brief])

print re[0]

