# -*- coding:utf-8 -*-
# 验证码:图片验证码,短信验证码
import re, random
from flask import request, abort, current_app, jsonify, \
    make_response, json
from . import api
from iHome.utils.captcha.captcha import captcha
from iHome import redis_store, constants
from iHome.utils.response_code import RET
from iHome.utils.SMS import CCP
from iHome.models import User


@api.route('/sms', methods=['POST'])
def send_sms():
    """:发送短信验证码
    1.获取参数并判断是否为空
    2.判断手机号是否合法
    3.取到redis总缓存的验证码内容,校验验证码
    4.手机号验证码校验
    5.生成短信验证码
    6.保存验证码
    7.发送成功
    :return:
    """
    # 1.获取参数并判断是否为空
    data = request.data
    data_dict = json.loads(data)
    mobile = data_dict.get('mobile')
    image_code = data_dict.get('image_code')
    image_code_id = data_dict.get('image_code_id')

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    # 2.判断手机号是否合法
    if not re.match(r'^1[34578][0-9]{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='电话号码格式错误')

    # 3.取到redis总缓存的验证码内容, 校验验证码
    try:
        real_image_code = redis_store.get('ImageCode_'+image_code_id)
        # 3.1 校验验证码
        if real_image_code.lower() != image_code.lower():
            return jsonify(errno=RET.DATAERR, errmsg='验证码错误')
        # 3.2 删除验证码
        redis_store.delete('ImageCode_'+image_code_id)
    except Exception as e:
        # 验证码过期
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取验证码失败')

    # 4.校验手机号
    try:
        user = User.query.filter_by(mobile=mobile).first()
        if user:
            return jsonify(errno=RET.DATAEXIST, errmsg='手机号已被注册')
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(errno=RET.DATAERR, errmsg='数据库错误')

    # 5.生成短信验证码,发送
    sms_code = random.randint(0, 999999)
    sms_code = '%06d' % sms_code
    current_app.logger.debug('短信验证码: %s' % sms_code)
    # 云通讯过期时间单位为分钟
    result = CCP().send_text_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], '1')
    if result == 0:
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信验证码失败')

    # 6.保存短信码到redis,以便后续验证
    try:
        redis_store.set('SMS_'+mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存验证码失败')

    # 7.发送成功
    return jsonify(errno=RET.OK, errmsg='发送成功')


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
    current_app.logger.debug(text)
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
