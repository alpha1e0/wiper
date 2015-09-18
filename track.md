
## 问题列表

* windows系统 static/attachment/汉字识别问题，webpy解析url存在问题，当URL中有中文时，webpy没有进行utf-8之类的解码；导致附件名称不能有中文

---

## 备注

编写model部分
自动化模块前端、后端整改
	子域扫描模块，包括域传送、dnsbrute、google hacking、http识别；页面整改成类似扫描器，分一键扫描和高级设置
	C段扫描模块，单独一个tab页面，自动聚合IP、手动添加IP，http识别；页面整改，两个框加入/删除按钮
datasave模块整改，需要支持多进程并发访问
init中log整改，扫描进程拥有自己的私有log




---

## 功能开发

1、完善自动化模块功能：

	C段扫描、
	域传送、
	googlehacking、
	http 指纹检测：区分http、https，自动获取网站title、判断服务器类型、操作系统类型、中间件检测、
	获取host操作系统、web服务器等信息

	备份、打包文件检测
	fckedit、ewebedit等检测
	CMS检测
	CMS hacking

2、客户端参数校验

3、数据库相关

	数据库使用脚本创建
	** 支持sqlite数据库

4、安装脚本编写
	
	判断isInstalled
	readme、copyright编写

5、其他
	

	不同level，标记不同颜色
	添加”显示host信息“按钮

	注释


## 其他

