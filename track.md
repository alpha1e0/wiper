
## 问题列表

* 参数校验，服务器端使用python修饰器，客户端使用类似机制

* static/attachment/汉字识别问题，webpy解析url存在问题，当URL中有中文时，webpy没有进行utf-8之类的解码；导致附件名称不能有中文

* "自动化"tab，每次进入的时候都会刷新页面，应该current不变则不刷新页面；给current定义一个“快照”功能，每次判断快照内容和当前内容是否一致

* 单击“项目”tab时，是否也要listProject

* 暂时ping不通的主机怎么处理

* 数据库使用脚本创建，全局isInstalled参数

* mysql删除不存在的记录会返回成功，这样如何确定删除记录成功？



---

1、参数验证

2、去掉http://字符串

3、完善功能：

	C段扫描、
	域传送、
	googlehacking、
	http ping（需要能够区分http、https），自动获取网站title
	ping工具

4、工具自动填充参数


---

上下文管理器实现参数检测

上下文管理器实现数据库查询，增加sqlexec、sqlquery上下文管理器，with sqlexec(sqlcmd) as result: if result: do something