# -*- coding:utf-8 -*-
from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

# 创建静态文件访问的蓝图
html = Blueprint('html', __name__)


# 定义静态文件访问的路由
# http://127.0.0.1/index.html
# http://127.0.0.1/my.html
# http://127.0.0.1/favicon.ico
@html.route('/<re(".*"):file_name>')
def get_html_file(file_name):
    """定义静态文件访问路径"""
    # 如果是根目录转到index
    if not file_name:
        file_name = 'index.html'
    # 当加载文件是标题栏logo时,不用加html前缀,直接搜索
    if file_name != 'favicon.ico':
        # 拼接文件名
        file_name = 'html/' + file_name

    # 通过current_app查找到查到静态文件下的html文件,并发送
    # 1.生成csrf_token
    csrf_token = generate_csrf()
    # 2.添加csrf_token到cookie中
    response = make_response(current_app.send_static_file(file_name))
    response.set_cookie('csrf_token', csrf_token)
    return response
