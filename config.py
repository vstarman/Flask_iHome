# -*- coding:utf-8 -*-
import redis


class Config(object):
    """工厂配置基类"""
    # 设置csrf秘钥
    SECRET_KEY = 'Fd7ygWLwQ3cFVRgt9gjejniDdQKhVfZjC2bIHtS3/+dleW3QI5CTlZRb6MFJdsV2'

    # 配置数据库链接
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.23.150:3306/Flask_iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # 关闭修改跟踪

    # 配置redis
    REDIS_HOST = '192.168.23.150'
    REDIS_PORT = 6379

    # Session扩展配置,默认保存在客户cookie里
    SESSION_TYPE = 'redis'      # 指定session保存方式:redis
    SESSION_USE_SIGNER = True   # 加密cookie中的session_id
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)   # 使用redis实例
    PERMANENT_SESSION_LIFETIME = 86400   # session有效期


class DevelopmentConfig(Config):
    """开发阶段使用的配置"""
    # 开启调试模式
    DEBUG = True

    # 配置数据库链接
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.23.150:3306/Flask_iHome'

    # 配置redis
    REDIS_HOST = '192.168.23.150'


class ProductionConfig(Config):
    """生产环境所需要的配置"""
    # 配置数据库链接
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/Flask_iHome'

    # 配置redis
    REDIS_HOST = '127.0.0.1'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}