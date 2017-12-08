# -*- coding:utf-8 -*-
# 实现用户注册,登录功能
from flask import request, current_app, jsonify, session
from . import api
from iHome import redis_store, db
from iHome.utils.response_code import RET
from iHome.models import User


@api.route('/users', methods=['POST'])
def register():
    """注册逻辑实现
    1.获取数据并判断不为空;
    2.取出本地手机验证码;
    3.与传入的验证码校验;
    4.创建用户模型,保存信息到数据库;
    5.返回响应
    :return:
    """
    # 1.获取数据并判断不为空;
    # data = request.data
    # json_dict = json.loads(data)
    json_dict = request.json
    mobile = json_dict.get('mobile')
    sms_code = json_dict.get('phonecode')
    password = json_dict.get('password')
    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='数据不完整')

    # 2.取出本地手机验证码;
    try:
        sms_code2 = redis_store.get('SMS_'+mobile)
        redis_store.delete('SMS_'+mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取手机号错误')

    if not sms_code2:   # 验证码已过期
        return jsonify(errno=RET.NODATA, errmsg='验证码已过期')

    # 3.与传入的验证码校验;
    if sms_code != sms_code2:
        return jsonify(errno=RET.PARAMERR, errmsg='手机验证码错误')

    # 4.创建用户模型, 保存信息到数据库;
    user = User()
    user.mobile = mobile
    user.name = mobile
    user.password = password

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据存储失败')

    # 5.保存信息到session
    session['user_id'] = user.id
    session['user_name'] = user.mobile
    session['user_mobile'] = user.mobile

    return jsonify(errno=RET.OK, errmsg='注册成功')


@api.route('/session', methods=['POST'])
def login():
    """登录逻辑实现
    1.获取手机号和密码
    2.校验手机号和密码
    3.保存登录结果
    4.返回结果
    :return:
    """
    # 1.获取手机号和密码
    get = request.json.get
    mobile = get('mobile')
    password = get('password')

    # 2.校验手机号和密码
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='数据不齐全')
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库错误')

    if not user:
        return jsonify(errno=RET.DATAEXIST, errmsg='用户不存在')

    # 2.1 校验密码
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='用户名或密码错误')

    # 3.保存登录结果
    session['user_name'] = user.name
    session['user_mobile'] = user.mobile
    session['user_id'] = user.id

    # 4.返回结果
    return jsonify(errno=RET.OK, errmsg='登陆成功')