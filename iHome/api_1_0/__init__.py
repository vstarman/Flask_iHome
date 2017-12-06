# -*- coding:utf-8 -*-
from flask import Blueprint

# 初始化蓝图对象
api = Blueprint('api_1_0', __name__)

from . import verify
