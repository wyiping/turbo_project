# -*- coding:utf-8 -*-

from pymongo import MongoClient

mc = MongoClient(host='localhost')
import gridfs
test_files = gridfs.GridFS(mc['test_files'])

# qiandao
qiandao = mc['qiandao']
