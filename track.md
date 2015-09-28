
## 问题列表

* windows系统 static/attachment/汉字识别问题，webpy解析url存在问题，当URL中有中文时，webpy没有进行utf-8之类的解码；导致附件名称不能有中文
* 删除host时没有刷新hostlist

---

## 备注

自动化模块前端、后端整改
	子域扫描模块，包括域传送、dnsbrute、google hacking、http识别；页面整改成类似扫描器，分一键扫描和高级设置
	C段扫描模块，单独一个tab页面，自动聚合IP、手动添加IP，http识别；页面整改，两个框加入/删除按钮


增加设置页面，上传字典文件放到设置页面

函数修饰器优化application.py代码

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

3、数据库相关

	** 支持sqlite数据库

4、安装脚本编写
	
	判断isInstalled
	readme、copyright编写

5、其他
	

	不同level，标记不同颜色
	添加”显示host信息“按钮

	注释


## 其他

