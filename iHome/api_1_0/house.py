# -*- coding:utf-8 -*-
# 房屋信息设置
from . import api
from flask import current_app, jsonify, request, g
from iHome.utils.response_code import RET
from iHome.utils.storage_image import storage_image
from iHome.models import Area, House, Facility, HouseImage
from iHome import db, redis_store
from iHome import constants
from iHome.utils.common import login_require


@api.route('/house/<int:house_id>/images', methods=["POST"])
@login_require
def upload_house_image(house_id):
    """
    1.接收参数:房屋id和要上穿的图片
    2.获取房屋对象
    3.上传图片
    4.若没有首页图片,将图片加到房屋对象上,并加入房屋图片表
    :param house_id: 房屋id
    :return:
    """
    # 1.接收参数:房屋id和要上穿的图片
    try:
        house_image_file = request.files.get('house_image').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='房屋图片参数错误')

    # 2.获取房屋对象
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋信息失败')

    if not house:
        return jsonify(errno=RET.NODATA, errmsg='房屋信息不存在')

    # 3.上传图片
    try:
        url = storage_image(house_image_file)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='房屋图片上传七牛云失败')

    # 4.若没有首页图片, 将图片加到房屋对象上, 并加入房屋图片表
    if house.index_image_url == '':
        house.index_image_url = url

    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = url

    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存房屋图片到数据库失败')

    return jsonify(errno=RET.OK, errmsg='OK', data={'url': constants.QINIU_DOMIN_PREFIX + url})


@api.route('/house', methods=['POST'])
@login_require
def add_new_house():
    """
    1.获取前端发送过来的json数据
    2.校验参数
    3.初始化House对象
    4.将信息保存到数据库
    5.返回成功响应
    :return:
    前端发来的数据:{
        title:1
        price:1
        area_id:1
        address:1
        room_count:1
        acreage:1
        unit:1
        capacity:1
        beds:1
        deposit:1
        min_days:1
        max_days:1
        facility:1
    }
    """
    # 1.获取前端发送过来的json数据
    user_id = g.user_id
    get = request.json.get
    title = get('title')
    price = get('price')
    area_id = get('area_id')
    address = get('address')
    room_count = get('room_count')
    acreage = get('acreage')
    unit = get('unit')
    capacity = get('capacity')
    beds = get('beds')
    deposit = get('deposit')
    min_days = get('min_days')
    max_days = get('max_days')

    # 2.校验参数
    if not all([title, price, address, area_id, room_count, acreage,
                unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    # 2.1 将房租和押金16.99等数字转化为整形保存(数据库字段为整形)
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数格式不正确')

    # 3.初始化House对象
    house = House()
    house.user_id = user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    # 3.1 将房屋设施选项为设施表外键,只保存设施id就好
    facility_list = get('facility')
    if facility_list:
        house.facilities = Facility.query.filter(Facility.id.in_(facility_list)).all()

    # 4.将信息保存到数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='添加房屋信息失败')

    # 5.返回成功响应
    return jsonify(errno=RET.OK, errmsg='房屋信息添加成功', data={'house_id': house.id})


@api.route('/areas')
def get_areas():
    """new_house视图的城区信息获取
    1.获取数据库城区信息
    2.将城区信息保存到redis中
    3.返回响应状态
    :return:
    """
    # 0.先从redis中获取areas
    try:
        areas_list = redis_store.get('areas')
        if areas_list:
            # eval 将字符串转为列表
            return jsonify(errno=RET.OK, errmsg='地区信息发送成功', data={'areas': eval(areas_list)})
    except Exception as e:
        current_app.logger.error(e)

    # 1.获取数据库城区信息
    areas = Area.query.all()
    # 对象不能直接传,转成json字典的列表
    areas_list = []
    for i in areas:
        areas_list.append(i.to_dict())

    # 2.将城区信息保存到redis中
    try:
        redis_store.set('areas', areas_list, constants.AREA_INFO_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='redis存储城区信息失败')

    # 3.返回响应状态
    return jsonify(errno=RET.OK, errmsg='地区信息发送成功', data={'areas': areas_list})
