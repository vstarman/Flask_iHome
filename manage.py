# -*- coding:utf-8 -*-
from flask import Flask, session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from iHome import app, db, redis_store


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
