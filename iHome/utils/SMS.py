# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-  

from libs.yuntongxun.CCPRestSDK import REST
# import ConfigParser

# ���ʺ�
accountSid = '8aaf07086010a0eb01602c66b0f60ba2'

# ���ʺ�Token
accountToken = 'd96004da19db45788f4cea1acadf2ab9'

# Ӧ��Id
appId = '8aaf07086010a0eb01602c66b1510ba9'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿� 
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


class CCP(object):
    """����ģ�����"""
    def __new__(cls, *args, **kwargs):
        """�õ���ֻ��ʼ��һ��SDK"""
        if not hasattr(cls, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, args, kwargs)
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance

    def send_text_sms(self, to, data, temp_id):
        """
        ����ģ�����
        :param to: �ֻ�����
        :param data: �������� ��ʽΪ���� ���磺{'12', '34'}���粻���滻���� ''
        :param temp_id: ģ��Id
        :return:
        """
        result = self.rest.sendTemplateSMS(to, data, temp_id)
        if result.get('statusCode') == '000000':
            return 1    # ��ʾ���ͳɹ�
        else:
            return 0    # ��ʾ����ʧ��


# def sendTemplateSMS(to, datas, tempId):
#     """
#     ����ģ�����
#     :param to: �ֻ�����
#     :param datas: �������� ��ʽΪ���� ���磺{'12', '34'}���粻���滻���� ''
#     :param tempId: ģ��Id
#     :return:
#     """
#     # ��ʼ��REST SDK
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
