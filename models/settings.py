# -*- coding:utf-8 -*-

from db.conn import (
    qiandao as _qiandao,
    test_files as _test_files
)

MONGO_DB_MAPPING = {
    'db': {
        'qiandao': _qiandao,
    },
    'db_file': {
        'qiandao': _test_files,
    }
}