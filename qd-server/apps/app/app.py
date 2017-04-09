#-*- coding:utf-8 -*-

import turbo.log

from base import BaseHandler
from helpers import qiandao

qd = qiandao.qian_dao
logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def GET(self):
        op = self.get_argument('op', None)
        mobile = self.get_argument('mobile', None)
        if not op:
            self.render('index.html')
        elif op == 'login':
            if qd.chaxun(mobile):
                self._data = 'success'
            else:
                self.response_error('error')


class QiandaoHandler(BaseHandler):
    def GET(self):
        mobile = self.get_argument('mobile', None)
        op = self.get_argument('op', None)

        if not op:
            self.render('info.html', info=qd.find_qiandao(mobile))
        elif op == 'on':
            qd.on(mobile)
        elif op == 'off':
            qd.off(mobile)


class AdminHandler(BaseHandler):
    def get(self):
        self.render('admin.html', list=qd.find_all_auto())