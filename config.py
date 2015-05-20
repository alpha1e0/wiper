#!/usr/bin/env python

'''
Information probing tool for penetration test
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import logging
import ConfigParse

class Conf(object):

    def __init__(self):
        cp = ConfigParse.ConfigParse()
        cp.read('config.cfg')

        self.ROOT_DIR = cp.get('basic', 'project_path') 


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

conf = Conf()
log = initLog()
