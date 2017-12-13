# -*- coding:utf-8 -*-
# 房屋信息设置
import datetime
from . import api
from flask import current_app, jsonify, request, g, session
from iHome.utils.response_code import RET
from iHome.utils.storage_image import storage_image
from iHome.models import Area, House, Facility, HouseImage, Order
from iHome import db, redis_store
from iHome import constants
from iHome.utils.common import login_require


@api.route('/order', methods=['POST'])
def add_order():
    """
    1.获取参数:入住时间,离开时间,房屋id
    2.校验参数
    3.校验房屋id
    4.判断该时间段是否有订单
    5.实例化订单模型
    6.保存订单
    7.返回结果
    返回订单id
    :return:
    """

    pass
