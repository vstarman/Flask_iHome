# -*- coding:utf-8 -*-
from flask import Flask


class Config(object):
    """工厂配置基类"""
    DEBUG = True


app = Flask(__name__)
# 用定义的配置类,并从中加载配置
app.config.from_object(Config)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()

