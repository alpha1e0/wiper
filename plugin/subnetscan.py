#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os

from thirdparty import yaml

from plugin.lib.plugin import Plugin, PluginError
from plugin.lib.commons import Nmap
from model.model import Host


class SubnetScanPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(SubnetScanPlugin, self).__init__(*args, **kwargs)

        try:
            with open(os.path.join("plugin","config","portmapping.yaml"), "r") as fd:
                self.portDict = yaml.load(fd)
        except IOError:
            raise PluginError("cannot load portmapping configure file 'portmapping.yaml'")
        self.portList = [key for key in self.portDict]


    def _handle(self, data):
        try:
            hostStr = data['ip'] + "/24"
        except AttributeError:
            raise PluginError("SubnetScanPlugin plugin got an invalid model")
        portStr = ",".join([str(x) for x in self.portList])
        cmd = "nmap -n -PS{ports} -p{ports} {host} -oX -".format(
            ports=portStr, host=hostStr)
        result = Nmap.scan(cmd)

        for host in result:
            self.put(host)