#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 17:40
# @Author  : Brave
# @Desc    :
# @File    : __init__.py.py

import base64
from  hashlib import sha1
import urllib.parse
import  time
import uuid
import requests
import hmac

config = {
'ACCESS_KEY': 'LTAI2hwywIirKrvp',
    'ACCESS_KEY_SECRET': 'DOi1lCsCyybLz4okozMGGY1IPdMPRe',
    'ACCESS_URL': 'https://sms.aliyuncs.com',
    'SIGN_NAME': '系统',
    'TEMPLATE_CODE': 'SMS_33500151',
}


#阿里云SMS
class AliyunSMS(object):
    def __init__(self):
        self.access_id = config.get('ACCESS_KEY')
        self.access_secret = config.get('ACCESS_KEY_SECRET')
        self.url = config.get('ACCESS_URL')
    def sign(self,  access_key_secret, parameter):
        sorted_parameters = sorted(parameter.items(), key=lambda p: p[0])
        canonicalized_query_string = ''
        for (k, v) in sorted_parameters:
            canonicalized_query_string += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        string_to_sign = 'GET&%2F&' + self.percent_encode(canonicalized_query_string[1:])
        hash_str = hmac.new(bytes((access_key_secret + "&").encode("utf-8")), string_to_sign.encode('utf-8'), sha1)
        return base64.encodebytes(hash_str.digest()).strip()

    @staticmethod
    def percent_encode(encode_str):
        encode_str = str(encode_str)
        result = urllib.parse.quote(encode_str.encode('utf-8'), '')
        result = result.replace('+', '%20')
        result = result.replace('*', '%2A')
        result = result.replace('%7E', '~')
        return result

    def make_url(self, params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        parameters = {
            'Format': 'JSON',
            'Version': '2016-09-27',
            'AccessKeyId': self.access_id,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': timestamp,
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid1()),
        }

        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature
        url = self.url + "/?" + urllib.parse.urlencode(parameters)
        return url

#发送手机验证码
def send (to, code):

        aliyun = AliyunSMS()

        data = {
            'Action': 'SingleSendSms',
            'SignName': config.get('SIGN_NAME'),
            'TemplateCode': config.get('TEMPLATE_CODE'),
            'RecNum': to,
            'ParamString': {'code': code},
        }

        url = aliyun.make_url(data)
        response = requests.get(url)
        if response.status_code != 200:
            return False
