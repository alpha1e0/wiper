#!/usr/bin/env python

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

from config import conf


class ProjectManage(object):

    def __init__(self, projectName):
        self.projectName = projectName
        self.projectPath = os.path.join(conf.ROOT_PATH, projectName)
        self.logPath = os.path.join(self.projectPath, 'wiplog')

    def createProject(self):
        if os.path.ispath(self.projectPath):
            return True

        os.mkdir(self.projectPath)
        os.mkdir(self.logPath)


