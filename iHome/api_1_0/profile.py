# -*- coding:utf-8 -*-
from . import api
from flask import session, current_app, jsonify, request
from iHome.utils.response_code import RET
from iHome.utils.storage_image import storage_image
from iHome import constants


@api.route('/user/header')
def upload_header():
    """
    1.TODO 判断是否登录;
    2.获取要上传的文件;
    3.上传到七牛云;
    4.返回上传成功设为图片地址
    """

    # 1.TODO 判断是否登录;
    try:
        user_id = session.get('user_id')
        if not user_id:
            jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    except Exception as e:
        current_app.logger.error(e)

    # 2.获取要上传的文件;
    try:
        header_file = request.files.get('header').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='请选择上传头像')

    # 3.上传到七牛云;
    try:
        key = storage_image(header_file)
    except Exception as e:
        current_app.logger.erroe(e)
        return jsonify(errno=RET.THIRDERR, errmsg='头像上传到七牛云失败')

    # 4.返回上传成功设为图片地址
    return jsonify(errno=RET.OK, errmsg='头像上传成功',
                   data={'header_key': constants.QINIU_DOMIN_PREFIX+key})
