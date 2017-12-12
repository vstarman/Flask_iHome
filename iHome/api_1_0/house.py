# -*- coding:utf-8 -*-
# 房屋信息设置
from . import api
from flask import current_app, jsonify, request, g, session
from iHome.utils.response_code import RET
from iHome.utils.storage_image import storage_image
from iHome.models import Area, House, Facility, HouseImage
from iHome import db, redis_store
from iHome import constants
from iHome.utils.common import login_require

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@api.route('/houses')
def get_houses_list():
    """用来显示搜索出的房屋列表
    1.获取所有房屋
    2.将查询集转为字典的列表
    3.将数据返回
    var params = {
        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
    };
    :return:
    """
    get_arg = request.args.get
    aid = get_arg('aid', '')
    sd = get_arg('sd', '')
    ed = get_arg('ed', '')
    sk = get_arg('sk', '')
    p = get_arg('p', 1)

    # 1.获取所有房屋
    try:
        house_query = House.query
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库失败')

    # 对条件进行判断
    if sk == 'new':               # 最新上线
        houses = house_query.order_by(House.create_time.desc())
    elif sk == 'booking':         # 入住最多
        houses = house_query.order_by(House.order_count.desc())
    elif sk == 'price-inc':       # 价格 低-高
        houses = house_query.order_by(House.price)
    else:                         # 价格 高-低
        houses = house_query.order_by(House.price.desc())

    # 3.对房屋分页,参数:1->第几页数据,2->每页几条数据,3->是否报404错误
    paginate = houses.paginate(int(p), constants.HOUSE_LIST_PAGE_CAPACITY, False)
    # 取出paginate所有对象
    houses = paginate.items
    total_page = len(houses)

    # 2.将查询集转为字典的列表
    if houses:
        house_list = []
        for house in houses:
            house_list.append(house.to_basic_dict())
        # 3.将数据返回
        return jsonify(errno=RET.OK, errmsg='OK', data={'houses': house_list, 'total_page': total_page})

    return jsonify(errno=RET.NODATA, errmsg='无房屋数据')


@api.route('/house/index')
def get_house_index():
    """主页房屋图片幻灯片显示
    以订单数量倒叙排序
    # 1.redis中获取
    # 2.查询房屋数据
    # 3.数据缓存
    # 4.返回应答
    :return:
    """
    # 1.redis中获取
    try:
        houses_list = redis_store.get('index_house_pic')
        if houses_list:
            return jsonify(errno=RET.OK, errmsg='OK', data=eval(houses_list))
    except Exception as e:
        current_app.logger.error(e)

    # 2.查询房屋数据
    try:
        houses = House.query.order_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    # 将对象集合转为字典列表
    houses_list = []
    if houses:
        for house in houses:
            houses_list.append(house.to_basic_dict())
        # print '-'*50, len(houses_list)
        # 3.数据缓存
        try:
            redis_store.set('index_house_pic', houses_list, constants.HOME_PAGE_DATA_REDIS_EXPIRES)
        except Exception as e:
            current_app.logger.error(e)

    # 4.返回应答
    return jsonify(errno=RET.OK, errmsg='OK', data=houses_list)


@api.route('/house/<int:house_id>')
def house_detail(house_id):
    """房屋详情页
    需求:
    1.是否是房东,房东则不显示预定按钮
    2.所以需要user_id,传给前段
    3.查询房屋数据返回
    4.将房屋信息缓存
    :param house_id:
    :return:
    """
    # 获取user_id,未登录值设为-1
    user_id = session.get('user_id', -1)
    # 4.查询缓存
    try:
        house_dict = redis_store.get('house_detail_%d' % house_id)
        # 如果用户未登录
        if house_dict:
            return jsonify(errno=RET.OK, errmsg='OK', data={'house': house_dict, 'user_id': user_id})
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='从redis中获取房屋详情缓存失败')

    # 1.是否是房东,房东则不显示预定按钮
    # 3.查询房屋数据返回
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库失败')
    if not house:
        return jsonify(errno=RET.NODATA, errmsg='房屋数据不存在')
    house_dict = house.to_full_dict()

    # 4.设置缓存
    try:
        redis_store.set('house_detail_%d' % house_id, house_dict, constants.HOUSE_DETAIL_REDIS_EXPIRE_SECOND)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='缓存设置失败')

    return jsonify(errno=RET.OK, errmsg='OK', data={'house': house_dict, 'user_id': user_id})


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
