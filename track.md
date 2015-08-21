
## 问题列表

* static/attachment/汉字识别问题，webpy解析url存在问题，当URL中有中文时，webpy没有进行utf-8之类的解码；导致附件名称不能有中文

* "自动化"tab，每次进入的时候都会刷新页面，应该current不变则不刷新页面；给current定义一个“快照”功能，每次判断快照内容和当前内容是否一致

* 单击“项目”tab时，是否也要listProject