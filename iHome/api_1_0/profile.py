# -*- coding:utf-8 -*-
# 个人信息视图模块:上传到图片七牛云
from . import api
from flask import session, current_app, jsonify, request
from iHome.utils.response_code import RET
from iHome.utils.storage_image import storage_image
from iHome import constants
from iHome.models import User
from iHome import db


@api.route('/user/avatar', methods=['POST'])
def upload_avatar():
    """
    1.TODO 判断是否登录;
    2.获取要上传的文件;
    3.上传到七牛云;
    4.返回上传成功设为图片地址,
    5.将图片地址拼接到url后,发给前端
    """

    # 1.TODO 判断是否登录;
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
        return jsonify(errno=RET.DBERR, errmsg='保存用户头像失败')

    # 4.返回上传成功设为图片地址
    return jsonify(errno=RET.OK, errmsg='头像上传成功',
                   data={'avatar_key': constants.QINIU_DOMIN_PREFIX+key})
