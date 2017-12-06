# -*- coding:utf-8 -*-
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import config


# 配置数据库
db = SQLAlchemy()
# 配置redis
redis_store = None
# 配置csrf,校验表单,防止跨站请求伪造
csrf = CSRFProtect()


def create_app(config_name):
    """工厂方法:根据不同的参数,生产不同的app对象"""
    app = Flask(__name__)
    # 用定义的配置类,并从中加载配置
    _config = config[config_name]
    app.config.from_object(_config)
    # 配置Session
    Session(app)
    # 配置数据库
    db.init_app(app)
    # redis初始化
    global redis_store
    redis_store = redis.StrictRedis(host=_config.REDIS_HOST, port=_config.REDIS_PORT)
    # 配置Session
    Session(app)
    # 配置csrf,校验表单,防止跨站请求伪造
    csrf.init_app(app)

    # 注册蓝图
    from iHome import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')
    return app
