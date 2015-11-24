
## 问题列表

* windows系统 static/attachment/汉字识别问题，webpy解析url存在问题，当URL中有中文时，webpy没有进行utf-8之类的解码；导致附件名称不能有中文
* bing 搜索，http://wwww.bing.com/search?ie=utf-8&q=intitle%3Atorrent&num=10&first=0& 总是被”机器人检测“阻断

* /servicerecognize type=0时候，下发”服务识别“任务，macos python异常退出，多次下发时从第二次下发出现bug

* “项目详情”页面滚动问题

---

## 备注

增加设置页面，上传字典文件放到设置页面

编辑时候的自动填充功能

对nmap执行时间做限制

---

## 功能开发

1、完善自动化模块功能：

	- C段扫描、
	- 域传送、
	- googlehacking、
	- http 指纹检测：区分http、https，自动获取网站title、判断服务器类型、操作系统类型、中间件检测、
	获取host操作系统、web服务器等信息

	备份、打包文件检测
	fckedit、ewebedit等检测
	CMS检测
	CMS hacking

2、小工具开发
	
	- exploit搜索

	whois、ip搜索工具

	编码/解码工具，支持：
		进制转换
		ascii/utf-8/gbk
		url编码/base64编码/HTML编解码
		MD5

	常用链接

3、数据库相关

	支持按project导入、导出（使用pickle或json）

4、安装脚本编写

-

5、其他
	
	readme、copyright编写


## 其他

性能优化：
	
	plugin做成生成器，每处理玩一个立刻路由给下游plugin
