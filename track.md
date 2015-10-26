
## 问题列表

* windows系统 static/attachment/汉字识别问题，webpy解析url存在问题，当URL中有中文时，webpy没有进行utf-8之类的解码；导致附件名称不能有中文
* bing 搜索，http://wwww.bing.com/search?ie=utf-8&q=intitle%3Atorrent&num=10&first=0& 总是被”机器人检测“阻断
* model中where，orderby多线程会出问题，应该用threading.local解决，

---

## 备注

自动化模块前端、后端整改
	子域扫描模块，包括域传送、dnsbrute、google hacking、http识别；页面整改成类似扫描器，分一键扫描和高级设置
	C段扫描模块，单独一个tab页面，自动聚合IP、手动添加IP，http识别；页面整改，两个框加入/删除按钮

增加设置页面，上传字典文件放到设置页面

Host中protocol改为字符串类型
Host中增加port
Model的方法有点乱，需要整改

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

2、小工具开发

	编码/解码工具，支持：
		进制转换
		ascii/utf-8/gbk
		url编码/base64编码/HTML编解码
		MD5

3、数据库相关

	支持按project导入、导出（使用pickle或json）

4、安装脚本编写
	
	readme、copyright编写

5、其他
	



## 其他

