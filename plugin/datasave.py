#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from config import RTD
from plugin.lib.plugin import Plugin
from model.model import Project, Host
from model.dbmanage import DBError


class DataSavePlugin(Plugin):
    def __init__(self, projectid, hostid=None, defaultValue={}, 
        *args, **kwargs):
        super(DataSavePlugin, self).__init__(*args, **kwargs)
        self.defaultValue = defaultValue
        self.projectid = projectid
        self.hostid = hostid

    def _handle(self, data):
        data['project_id'] = self.projectid
        for key,value in self.defaultValue.iteritems():
            data[key] = value
            
        host = Host(**data)
        host.save()
