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

# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12', '34'}���粻���滻���� ''
# @param $tempId ģ��Id


def sendTemplateSMS(to, datas, tempId):
    # ��ʼ��REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)
    
    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems(): 
        
        if k == 'templateSMS':
                for j, s in v.iteritems(): 
                    print '%s:%s' % (j, s)
        else:
            print '%s:%s' % (k, v)
    
   
sendTemplateSMS(18832667432, ['12', '34'], '1')
