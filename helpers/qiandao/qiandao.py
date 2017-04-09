# -*- coding:utf-8 -*-

from models.qiandao import model
import json, urllib, urllib2, datetime, threading, time, random
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
                mes['schedule'] = self.find_one({'mobile':mobile})['schedule']
            else:
                mes['auto'] = False
            # while page < pagecount:
            #     page = page + 1
            #     res = self.query(mobile, str(page))
            #     for m in res['list']:
            #         mes['list'].append(m)
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
        t = threading_auto(mobile, getSchedule())
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

    def daemon(self):
        for d in self.find():
            self.remove({"mobile": d['mobile']})
            t = threading_auto(d['mobile'], getSchedule())
            t.start()

    def valid_today(self):
        pass


def getSchedule():
    rnum = random.randint(7, 12)
    if rnum < 10:
        H = ' 0' + str(rnum)
    else:
        H = ' ' + str(rnum)
    return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + H

class threading_auto(threading.Thread):
    def __init__(self, mobile, schedule):
        threading.Thread.__init__(self)
        self.mobile = mobile
        self.schedule = schedule

    def run(self):
        db = model.Qiandao()
        threadname = threading.currentThread().getName()
        db.insert({'mobile': self.mobile, 'threadname': threadname, 'schedule': self.schedule})
        signal[threadname] = True
        while signal[threadname]:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H")
            if now == self.schedule:
                QianDao().insert_qiandao(self.mobile)
                next_schedule = getSchedule()
                db.update({'mobile': self.mobile},{'$set':{'schedule': next_schedule}})
                self.schedule = next_schedule
            time.sleep(60 * 60)
