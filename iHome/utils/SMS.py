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

# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12', '34'}，如不需替换请填 ''
# @param $tempId 模板Id


def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
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
