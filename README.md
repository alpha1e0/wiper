# Wiper  ---  WEB渗透辅助工具

## 介绍

wiper是一个WEB渗透测试辅助工具，主要用于前期信息收集、攻击面分析。wiper能够以可视化的方式展示web渗透过程中收集的信息，对于一个给定的站点URL，wiper能够使用DNS域传送、Google Hacking、DNS爆破技术获取目标URL相关的信息，同时wiper支持C端扫描。

---

## 安装

从[这里](https://github.com/alpha1e0/wiper)下载最新版本，或使用命令

	git clone https://github.com/alpha1e0/wiper

clone到本地

wiper支持Windows/Linux/MacOS，需使用python **2.6.x** 或 **2.7.x**运行

### 依赖：

wiper的一些功能依赖于Nmap，因此需要安装[Nmap](http://insecure.org/)

Nmap会默认添加环境变量，如果希望自己修改Nmap路径，则可以修改data/config.yaml中nmap的路径，或者在web控制台中“设置--》其他”修改

---

## 使用

python wiper.py


