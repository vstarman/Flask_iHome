# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis


class Config(object):
    """项目的配置"""
    # 开启调试模式
    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/Flask_iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis配饰
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379


app = Flask(__name__)
# 从对象中加载配置
app.config.from_object(Config)
# 初始化数据库
db = SQLAlchemy(app)
# 初始化redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


@app.route('/index')
def index():
    # redis_store.set('name', 'xiaofang')
    return 'index'

if __name__ == '__main__':
    app.run()
