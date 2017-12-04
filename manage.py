# -*- coding:utf-8 -*-
import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
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
# 数据库迁移
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/', methods=['post', 'get'])
def index():
    session['name'] = 'xiaohua'
    redis_store.set('name', 'xiaoli')
    return 'index'


if __name__ == '__main__':
    # app.run()
    manager.run()
