# -*- coding:utf-8 -*-
# 验证码:图片验证码,短信验证码
from flask import request, abort, current_app, jsonify, make_response
from . import api
from iHome.utils.captcha.captcha import captcha
from iHome import redis_store, constants
from iHome.utils.response_code import RET


@api.route('/imagecode')
def get_image_code():
    """
    1.取到传入图片编码
    2.生成图片验证码
    3.存储到redis中(key是图片编码,值是验证码文字内容)
    4.返回图片
    :return:
    """
    # 1.取到传入的图片码
    args = request.args
    cur = args.get('cur')

    # 如果用户没传图片id直接抛错
    if not cur:
        abort(403)

    # 2.生成验证码
    _, text, image = captcha.generate_captcha()
    current_app.logger.debug(text)

    # 3.存储到redis中(key是图片编码,值是图片text内容)
    # redis_store.set('key', 'value', '过期时间')
    try:
        redis_store.set('ImageCode_' + cur, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        # 保存错误信息到log中
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg='图片保存失败')

    # 4.返回验证码图片,make_response为了为图片增加Content-Type
    response = make_response(image)
    return response
