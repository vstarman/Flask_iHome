# -*- coding:utf-8 -*-
# 个人信息视图模块:上传到图片七牛云
from . import api
from flask import session, current_app, jsonify, request, g
from iHome.utils.response_code import RET
from iHome.utils.storage_image import storage_image
from iHome.models import User
from iHome import db
from iHome import constants
from iHome.utils.common import login_require


@api.route('/user/auth', methods=['GET'])
@login_require
def get_auth_info():
    """实名认证,显示
    1.获取姓名,身份证号码
    2.设置到数据库
    3.返回状态
    :return:
    """
    user_id = g.user_id

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询当前登录用户失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    return jsonify(errno=RET.OK, errmsg='', data=user.set_auth_dict())


@api.route('/user/auth', methods=['POST'])
@login_require
def set_auth_info():
    """实名认证,显示
    1.获取姓名,身份证号码
    2.设置到数据库
    3.返回状态
    :return:
    """
    # 1.获取姓名, 身份证号码
    get = request.json.get
    real_name = get('real_name')
    id_card = get('id_card')

    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    # 2.获取用户对象,设置到数据库
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询当前登录用户失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    user.real_name = real_name
    user.id_card = id_card

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据库存储用户认证信息失败')

    # 3.返回状态
    return jsonify(errno=RET.OK, errmsg='', data=user.set_auth_dict())


@api.route('/user', methods=['GET'])
@login_require
def get_user_info():
    """用户信息修改中心
    0.校验登录状态:装饰其实现
    1.获取用户对象
    2.查询头像
    3.查询昵称
    4.返回ok
    :return:
    """
    # 0.校验登录状态
    # 1.获取用户对象
    try:
        user = User.query.get(session['user_id'])
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询当前登录用户失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    # 4.返回ok
    return jsonify(errno=RET.OK, errmsg='查询成功', data=user.to_auth_dict())


@api.route('/user/name', methods=['POST'])
@login_require
def set_user_name():
    """修改用户名
    1.验证是否登录
    2.获取要设置的用户名,并判空
    3.取到当前用户id并设置模型
    4.更新用户名信息到数据库
    5.返回成功响应
    :return:
    """
    # 1.验证是否登录

    # 2.获取要设置的用户名
    name = request.json.get('name')
    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg='请输入需要设置的名字')

    # 3.取到当前用户id并设置模型
    try:
        user = User.query.get(session['user_id'])
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询当前登录用户失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户未登录')

    # 4.更新用户名信息到数据库
    try:
        user.name = name
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='设置用户名到数据库失败')

    # 设置session
    session['name'] = name
    # 5.返回成功响应
    return jsonify(errno=RET.OK, errmsg='用户名设置成功')


@api.route('/user/avatar', methods=['POST'])
@login_require
def upload_avatar():
    """修改用户头像
    1.TODO 判断是否登录;
    2.获取要上传的文件;
    3.上传到七牛云;
    4.返回上传成功设为图片地址,
    5.将图片地址拼接到url后,发给前端
    """

    # 1.TOD 判断是否登录;
    # try:
    #     user_id = session.get('user_id')
    #     if not user_id:
    #         jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    # except Exception as e:
    #     current_app.logger.error(e)

    # 2.获取要上传的文件;
    try:
        avatar_file = request.files.get('avatar').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='请选择上传头像')

    # 3.上传到七牛云;
    try:
        key = storage_image(avatar_file)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='头像上传到七牛云失败')

    # 3.1 保存图片url到用户模型
    try:
        user = User.query.get(session['user_id'])
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询当前登录用户失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    user.avatar_url = key
    try:
        # 保存到数据库
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存用户头像失败')

    # 4.返回上传成功设为图片地址
    return jsonify(errno=RET.OK, errmsg='头像上传成功',
                   data={'avatar_key': constants.QINIU_DOMIN_PREFIX+key})
