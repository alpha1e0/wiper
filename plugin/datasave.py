#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from config import RTD
from plugin.lib.plugin import Plugin
from model.model import Project, Host, Vul, Comment
from model.dbmanage import DBError


class DataSavePlugin(Plugin):
    def __init__(self, projectid, hostid=None, log=True, defaultValue={}):
        super(DataSavePlugin, self).__init__(timeout=1, log=log)
        self.defaultValue = defaultValue
        self.projectid = projectid
        self.hostid = hostid

    def handle(self, data):
        try:
            if isinstance(data, Host):
                data.project_id = self.projectid
                for key,value in self.defaultValue.iteritems():
                    data[key] = value
                data.save()
            elif isinstance(data, Vul) or isinstance(data, Comment):
                data.host_id = self.hostid
                data.save()
            elif isinstance(data, Project):
                data.save()
        except DBError as error:
            if self.log:
                self.log.error("save model error"+str(error))