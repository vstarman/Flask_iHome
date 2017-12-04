# -*- coding:utf-8 -*-
import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# class Config(object):
#     """项目的配置"""
#     # 开启调试模式
#     DEBUG = True
#     # 数据库配置
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/Flask_iHome'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     # redis配置
#     REDIS_HOST = '192.168.23.150'
#     REDIS_PORT = 6379
#     # Session扩展设置
#     SESSION_TYPE = 'redis'   # 存储类型
#     SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)     # redis 的链接
#     SESSION_USE_
#


app = Flask(__name__)
# # 从对象中加载配置
# app.config.from_object(Config)
# # 初始化数据库
# db = SQLAlchemy(app)
# # 初始化redis
# redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# # 集成CSRF保护:提供校验cookie中csrf与表单提交过来的csrf是否一样
# csrf = CSRFProtect(app)
# # 集成session
# Session(app)
# # 集成数据库迁移


@app.route('/', methods=['post', 'get'])
def index():
    # session['name'] = 'xiaoHong'
    # redis_store.set('name', 'xiaofang')
    return 'index'

if __name__ == '__main__':
    app.run()
