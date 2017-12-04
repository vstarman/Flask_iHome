# -*- coding:utf-8 -*-
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)
# 用定义的配置类,并从中加载配置
app.config.from_object(Config)
# 配置数据库
db = SQLAlchemy(app)
# 配置redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 配置Session
Session(app)
# 配置csrf,校验表单,防止跨站请求伪造
CSRFProtect(app)
