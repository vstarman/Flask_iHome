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
    # 1.获取参数:入住时间,离开时间,房屋id
    get = request.json.get
    start_day_str = get('start_day')
    end_day_str = get('end_day')
    house_id = get('house_id')

    # 2.校验参数
    if not all([start_day_str, end_day_str, house_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        start_day = datetime.datetime.strptime(start_day_str, '%Y-%m-%d')
        end_day = datetime.datetime.strptime(end_day_str, '%Y-%m-%d')
        if start_day > end_day:
            return jsonify(errno=RET.PARAMERR, errmsg='入住时间不能大于退房时间')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 3.校验房屋id
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋信息出错')
    if not house:
        return jsonify(errno=RET.NODATA, errmsg='无此房屋信息')

    # 4.判断该时间段是否有订单
    try:
        filters = [Order.house_id == house_id, Order.begin_date < end_day, Order.end_date > start_day]
        # 查询冲突的订单
        houses = House.query.filter(*filters)
        if not houses:
            return jsonify(errno=RET.NODATA, errmsg='与已有订单时间重复,下单失败')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询失败')

    # 5.实例化订单模型
    days = (end_day - start_day).days
    order = Order()
    order.user_id = session.get('user_id')
    order.house_id = house_id
    order.begin_date = start_day
    order.end_date = end_day
    order.days = days
    order.house_price = house.price
    order.amount = house.price * days + house.deposit
    order.status = "WAIT_ACCEPT"
    # 给房屋订单属性+1
    house.order_count += 1

    # 6.保存订单
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据保存失败')

    # 7.返回结果
    return jsonify(errno=RET.OK, errmsg='OK')


@api.route('/user/orders')
@login_require
def get_user_orders():
    """用户:获取订单
    1.获取用户id, 用户role
    2.校验参数
    3.查询订单数据
    role = custom : 房客
        or landlord : 房东
    :return:
    """
    user_id = g.user_id
    role = request.args.get('role')

    if not role:
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    if role not in ('custom', 'landlord'):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        if role == 'custom':    # 用户查询自己订单
            orders = Order.query.filter(user_id == Order.user_id).all()
            if not orders:
                return jsonify(errno=RET.NODATA, errmsg='查询数据为空')

        else:    # 房东查询房客订单
            # 查询出所有自己的房屋
            houses = House.query.filter(House.user_id == user_id).all()
            if not houses:
                return jsonify(errno=RET.NODATA, errmsg='该用户无房屋')
            # 取出房屋id
            house_ids = [house.id for house in houses]
            # 筛选出是自己房屋id的订单
            orders = Order.query.filter(Order.house_id.in_(house_ids)).all()
            if not orders:
                return jsonify(errno=RET.NODATA, errmsg='该房东暂无用户订单')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    order_list = []
    for order in orders:
        order_list.append(order.to_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data={'orders': order_list})
