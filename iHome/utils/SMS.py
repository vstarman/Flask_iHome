# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-  

from libs.yuntongxun.CCPRestSDK import REST
# import ConfigParser

# 主帐号
accountSid = '8aaf07086010a0eb01602c66b0f60ba2'

# 主帐号Token
accountToken = 'd96004da19db45788f4cea1acadf2ab9'

# 应用Id
appId = '8aaf07086010a0eb01602c66b1510ba9'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口 
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


class CCP(object):
    """发送模板短信"""
    def __new__(cls, *args, **kwargs):
        """用单例只初始化一次SDK"""
        if not hasattr(cls, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, args, kwargs)
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance

    def send_text_sms(self, to, data, temp_id):
        """
        发送模板短信
        :param to: 手机号码
        :param data: 内容数据 格式为数组 例如：{'12', '34'}，如不需替换请填 ''
        :param temp_id: 模板Id
        :return:
        """
        result = self.rest.sendTemplateSMS(to, data, temp_id)
        if result.get('statusCode') == '000000':
            return 1    # 表示发送成功
        else:
            return 0    # 表示发送失败


# def sendTemplateSMS(to, datas, tempId):
#     """
#     发送模板短信
#     :param to: 手机号码
#     :param datas: 内容数据 格式为数组 例如：{'12', '34'}，如不需替换请填 ''
#     :param tempId: 模板Id
#     :return:
#     """
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#
#         if k == 'templateSMS':
#                 for j, s in v.iteritems():
#                     print '%s:%s' % (j, s)
#         else:
#             print '%s:%s' % (k, v)


if __name__ == '__main__':
    CCP().send_text_sms('18832667432', ['888888', 100], 1)
    # sendTemplateSMS('18832667432', ['888888', 100], 1)
