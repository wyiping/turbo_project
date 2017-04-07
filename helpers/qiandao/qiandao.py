# -*- coding:utf-8 -*-

from models.qiandao import model
import json, urllib, urllib2, datetime, threading, time
MODEL_SLOTS = ['QianDao']

signal = {}

class QianDao(model.Qiandao):

    def find_qiandao(self, mobile):
        page = 1
        mes = self.query(mobile)
        pagecount = mes['pageCount']
        if mes.get('list'):
            if self.find({'mobile': mobile}).count() > 0:
                mes['auto'] = True
            else:
                mes['auto'] = False
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

    def on(self, mobile):
        sched_Timer = (datetime.datetime.now() + datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H")
        if sched_Timer > datetime.datetime.now().strftime("%Y-%m-%d") + " 07":
            sched_Timer = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + " 07"

        t = threading_auto(mobile, sched_Timer)
        t.start()

    def off(self, mobile):
        user = self.find_one({'mobile': mobile})
        self.remove({"mobile": mobile})
        signal[user['threadname']] = False

    def find_all_auto(self):
        data = []
        for t in self.find():
            data.append(t)
        for item in threading.enumerate():
            print item
        return data

class threading_auto(threading.Thread):
    db = model.Qiandao()
    def __init__(self, mobile, sched_Timer):
        threading.Thread.__init__(self)
        self.mobile = mobile
        self.sched_Timer = sched_Timer

    def run(self):
        threadname = threading.currentThread().getName()
        self.db.insert({'mobile': self.mobile, 'threadname': threadname})
        signal[threadname] = True
        flag = 0
        while signal[threadname]:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H")
            if now == self.sched_Timer:
                flag = 1
                QianDao().insert_qiandao(self.mobile)
            else:
                if flag == 1:
                    flag = 0
                    self.sched_Timer = (datetime.datetime.strptime(self.sched_Timer, "%Y-%m-%d %H") + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H")
            time.sleep(60 * 60)
