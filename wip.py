#!/usr/bin/env python

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import logging


def initLog():
    '''
    critical, error, warning, info, debug, notset
    '''
    log = logging.getLogger('wip')
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(os.path.join(conf.ROOT_DIR, 'wiplog.log'))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)

    return log

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


