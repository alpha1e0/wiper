#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import socket
import re

from plugin.lib.commons import DnsBrute
from plugin.lib.plugin import Plugin, PluginError
from model.model import Host
from config import RTD, CONF


class DnsBrutePlugin(Plugin):
    '''
    Use wordlist to bruteforce subdomain.
    '''
    def __init__(self, dictlist, bruteTopDomain=False, *args, **kwargs):
        super(DnsBrutePlugin, self).__init__(*args, **kwargs)

        self.urlPattern = re.compile(r"^(?:http(?:s)?\://)?((?:[-0-9a-zA-Z_]+\.)+(?:[-0-9a-zA-Z_]+))")
        dictlist = dictlist if dictlist else ["subdomain_default.txt"]
        self.dictlist = [os.path.join("data","wordlist","dnsbrute",x) for x in dictlist]
        self.bruteTopDomain = bruteTopDomain


    def _handle(self, data):
        if not isinstance(data, Host):
            self.put(data)
            return
        
        try:
            dataDomain = self.urlPattern.match(data.url).groups()[0].lower()
        except AttributeError:
            raise PluginError("dns brute plugin, domain format error")

        for item in DnsBrute(dataDomain, self.dictlist, self.bruteTopDomain):
            self.put(Host(**item))
        

