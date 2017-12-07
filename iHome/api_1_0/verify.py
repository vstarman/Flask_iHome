# -*- coding:utf-8 -*-
# 验证码:图片验证码,短信验证码
from flask import request, abort, current_app, jsonify, make_response
from . import api
from iHome.utils.captcha.captcha import captcha
from iHome import redis_store, constants
from iHome.utils.response_code import RET

#
# @api.route('/sms', method=['POST'])
# def send_sms():
#     """:发送短信验证码
#     1.获取参数并判断是否为空
#     2.判断手机号是否合法
#     3.取到redis总缓存的验证码内容,校验验证码
#     4.生成短信验证码
#     5.给前端响应结果
#     :return:
#     """
    # 1.获取参数并判断是否为空
    # data =




@api.route('/imagecode')
def get_image_code():
    """:发送图片验证码
    1.取到传入图片编码
    2.生成图片验证码
    3.存储到redis中(key是图片编码,值是验证码文字内容)
    4.返回图片
    :return:
    """
    # 1.取到传入的图片码
    args = request.args
    cur = args.get('cur')
    pre = args.get('pre')

    # 如果用户没传图片id直接抛错
    if not cur:
        abort(403)

    # 2.生成验证码
    _, text, image = captcha.generate_captcha()

    # 3.存储到redis中(key是图片编码,值是图片text内容)
    # redis_store.set('key', 'value', '过期时间')
    try:
        if pre:
            # current_app.logger.debug(pre)
            redis_store.delete('ImageCode_'+pre)
        redis_store.set('ImageCode_'+cur, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        # 保存错误信息到log中
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg='图片保存失败')

    # 4.返回验证码图片,make_response为了为图片增加Content-Type
    response = make_response(image)
    # 设置Content-Type
    response.headers['Content-Type'] = 'image/jpg'
    return response
