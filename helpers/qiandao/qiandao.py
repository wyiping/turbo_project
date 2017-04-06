# -*- coding:utf-8 -*-

# from datetime import datetime, timedelta

from pymongo import DESCENDING, ASCENDING

from helpers import settings

import json, urllib, urllib2, datetime

MODEL_SLOTS = ['QianDao']


class QianDao():

    def find_qiandao(self,mobile):
        page = 1
        url_qiandao = 'http://zhaopin.0fafa.com/work/doudou/shixi/qiandao.php?mobile='
        mes = json.loads(urllib2.urlopen(url_qiandao + mobile+'&page='+str(page), timeout=5).read())
        pageSize = mes['pageCount']
        if self.check_today(mes['list'][0]['addtime'][0:10]):
            self.find_all_qiandao(mes,page,pageSize,url_qiandao,mobile)
            return mes
        else:
            self.insert_qiandao(mes)
            self.find_qiandao(mobile)

    def find_all_qiandao(self,mes,page,pageSize,url,mobile):
        while page < pageSize:
            page = page + 1
            res = json.loads(urllib2.urlopen(url + mobile + '&page=' + str(page), timeout=5).read())
            for m in res['list']:
                mes['list'].append(m)

    def insert_qiandao(self,mes):
        data = urllib.urlencode({'mobile': mes['list'][0]['mobile'], 'content': mes['list'][0]['content'].encode('utf-8'), 'image': '', 'jindu': mes['list'][0]['jindu'], 'weidu': mes['list'][0]['weidu']})
        req = urllib2.urlopen(urllib2.Request('http://zhaopin.0fafa.com/work/doudou/shixi/insert_qiandao.php?' + data, headers={"User-Agent": "11.5.78 rv:0.0.1 (iPhone; iPhone OS 9.3.5; zh_CN)"}))
        return req.read()

    def check_today(self,addTime):
        if addTime != datetime.datetime.now().strftime('%Y-%m-%d'):
            return False
        else:
            return True
