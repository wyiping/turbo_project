#-*- coding:utf-8 -*-

import turbo.log

from base import BaseHandler
from helpers import qiandao

qd = qiandao.qian_dao
logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self):
        self.render('index.html')

class QiandaoHandler(BaseHandler):
    def get(self):
        mobile = self.get_argument('mobile',None)
        self.render('qiandao.html', qiandao=qd.find_qiandao(mobile))