# -*- coding:utf-8 -*-

# from datetime import datetime, timedelta

from pymongo import DESCENDING, ASCENDING

from helpers import settings

import json, urllib, urllib2, datetime, multiprocessing, time
MODEL_SLOTS = ['QianDao']


class QianDao():

    def find_qiandao(self,mobile):
        page = 1
        mes = self.query(mobile)
        pagecount = mes['pageCount']
        if mes.get('list'):
            while page < pagecount:
                page = page + 1
                res = self.query(mobile, str(page))
                for m in res['list']:
                    mes['list'].append(m)
            return mes
        else:
            return {'error': '号码有误'}

    def query(self, mobile='', page='1', url='http://zhaopin.0fafa.com/work/doudou/shixi/qiandao.php?mobile='):
        return json.loads(urllib2.urlopen(url + mobile+'&page='+page).read())

    def insert_qiandao(self, mobile):
        mes = self.query(mobile)
        data = urllib.urlencode({'mobile': mes['list'][0]['mobile'], 'content': mes['list'][0]['content'].encode('utf-8'), 'image': '', 'jindu': mes['list'][0]['jindu'], 'weidu': mes['list'][0]['weidu']})
        return urllib2.urlopen(urllib2.Request('http://zhaopin.0fafa.com/work/doudou/shixi/insert_qiandao.php?' + data, headers={"User-Agent": "11.5.78 rv:0.0.1 (iPhone; iPhone OS 9.3.5; zh_CN)"}))

    def sched(self, mobile, sched_Timer):
        flag = 0
        while 1:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H")
            print sched_Timer,now
            if now == sched_Timer:
                flag = 1
                self.insert_qiandao(mobile)
            else:
                if flag == 1:
                    flag = 0
                    sched_Timer = (datetime.datetime.strptime(sched_Timer,"%Y-%m-%d %H") + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H")
            time.sleep(60*60)

    def auto(self, mobile):
        sched_Timer = (datetime.datetime.now() + datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H")
        if sched_Timer < datetime.datetime.now().strftime("%Y-%m-%d") + " 07":
            pass
        else:
            sched_Timer = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + " 07"
        p = multiprocessing.Process(target=self.sched, args=(mobile, sched_Timer))
        p.start()
        print "p.pid:", p.pid
        print "p.name:", p.name
        print "p.is_alive:", p.is_alive()
