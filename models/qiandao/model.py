#-*- coding:utf-8 -*-

from base import *

class Qiandao(Model):

    """
    email: user account
    passwd: user account passwd
    atime: added time
    """
    name = 'auto'
    
    field = {
        'mobile': (basestring, ''),
        'threadname': (basestring, ''),
    }

