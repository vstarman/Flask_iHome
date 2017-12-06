# -*- coding:utf-8 -*-
from flask import Blueprint, current_app

html = Blueprint('html', __name__)


# 定义静态文件访问路径
@html.route('/<re(".*"):file_name>')
def get_html_file(file_name):
    # 如果是根目录转到index
    if not file_name:
        file_name = 'index.html'
    # 当加载文件是标题栏logo时,不用加html前缀,直接搜索
    if file_name != 'favicon.ico':
        # 拼接文件名
        file_name = 'html/' + file_name
    # 通过current_app查找到查到静态文件下的html文件,并发送
    return current_app.send_static_file(file_name)
