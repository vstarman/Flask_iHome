# -*- coding:utf-8 -*-
import redis
import logging
from logging.handlers import RotatingFileHandler
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

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


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

    # 配置csrf,校验表单,防止跨站请求伪造
    csrf.init_app(app)

    # 注册蓝图
    from iHome import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')

    # 注册html静态资源文件蓝图
    from web_html import html
    app.register_blueprint(html)
    return app
