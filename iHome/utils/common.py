# -*- coding:utf-8 -*-
# 通用工具:
# 用来定义正则, 登录装饰器
from flask import session, jsonify, current_app, g
from werkzeug.routing import BaseConverter
from iHome.utils.response_code import RET
import functools


class RegexConverter(BaseConverter):
    """自定义正则转换器"""
    def __init__(self, url_map, *args, **kwargs):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def login_require(f):
    @functools.wraps(f)     # 修饰内层函数,防止装饰器修改内层函数的__name__属性
    def wrapper(*args, **kwargs):
        try:
            user_id = session.get('user_id')
            g.user_id = user_id
            if not user_id:
                return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
        except Exception as e:
            current_app.logger.error(e)
        return f(*args, **kwargs)
    return wrapper
