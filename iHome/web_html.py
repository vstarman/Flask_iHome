# -*- coding:utf-8 -*-
from flask import Blueprint, current_app

html = Blueprint('html', __name__)


# 定义静态文件访问路径
@html.route('/<file_name>')
def get_html_file(file_name):
    # 拼接文件名
    file_name = 'html/' + file_name
    # 通过current_app查找到查到静态文件下的html文件,并发送
    return current_app.send_static_file(file_name)
