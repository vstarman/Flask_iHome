# -*- coding:utf-8 -*-

import logging
from flask import session, current_app
from . import api
from iHome import redis_store


@api.route('/', methods=['post', 'get'])
def index():
    session['name'] = 'xiaohua'
    redis_store.set('name', 'xiaoli')
    # 其他项目使用
    logging.debug('DEBUG LOGLOG')
    print '='*50
    # flask内置,信息更详细
    current_app.logger.debug('LOG LOG CURRENT')
    return 'index'
