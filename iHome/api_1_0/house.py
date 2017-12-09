# -*- coding:utf-8 -*-
# 房屋信息设置
from . import api
from flask import session, current_app, jsonify, request, g
from iHome.utils.response_code import RET
from iHome.utils.storage_image import storage_image
from iHome.models import User, Area
from iHome import db
from iHome import constants
from iHome.utils.common import login_require


@api.route('/areas')
def get_areas():
    """new_house视图的城区信息获取
    1.获取数据库城区信息
    3.返回响应状态
    :return:
    """
    # 1.获取数据库城区信息
    areas = Area.query.all()
    # 对象不能直接传,转成json字典的列表
    areas_list = []
    for i in areas:
        areas_list.append(i.to_dict())

    # 3.返回响应状态
    return jsonify(errno=RET.OK, errmsg='地区信息发送成功', data={'areas': areas_list})
