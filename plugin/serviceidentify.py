#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import re

from thirdparty import yaml
from thirdparty import requests
from thirdparty.BeautifulSoup import BeautifulSoup

from plugin.lib.plugin import Plugin, PluginError
from plugin.lib.nmapwrapper import Nmap
from model.model import Host
from config import CONF


class ServiceIdentifyPlugin(Plugin):
    '''
    Service identify plugin.
    Input:
        log: whether to log
        ptype: plugin running type.
            0: default, recognize service with default portList
            1: do not scan port, just do http recognize
            2: scan nmap inner portList
            3: scan 1-65535 port
    '''
    def __init__(self,log=True,ptype=0):
        super(ServiceIdentifyPlugin, self).__init__(log=log)

        self.ptype = ptype


    def handle(self, data):
        if not isinstance(data, Host):
            self.put(data)
        else:
            for host in ServiceIdentify(self.ptype, **data):
                if 'description' in data: host.description = data.description
                if 'level' in data: host.level = data.level
                if host.get('protocol',None) in ['http','https']:
                    if 'url' in data: host.url = data.url
                    if 'title' in data: host.title = data.title

                self.put(Host(**host))

