# -*- encoding: utf-8 -*-
'''
@File    :   trans.py
@Time    :   2020/09/09 20:42:07
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicso@wicos.cn
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Blog    :   https://www.wicos.me
'''

# here put the import lib
import requests as rq
import random
import hashlib

from skimage import data

class Trans:
    def __init__(self,appid,secretKey):
        self.appid = appid
        self.secretKey = secretKey
        self.session = rq.Session()
        self.url = "https://fanyi-api.baidu.com/api/trans/vip/fieldtranslate"
        self.session.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def mix(self):
        salt = salt = random.randint(32768, 65536)
        self.salt = salt
        sign = self.appid + self.trans_data + str(salt) + self.domain + self.secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        self.sign = sign
        #return sign

    def start_trans(self,trans_data,tolang,domain,fromlang = None):
        self.trans_data  =trans_data
        self.tolang = tolang
        self.domain = domain
        if fromlang:
            self.fromlang = fromlang
        else:
            self.fromlang = "auto"
        self.mix()
        post_data = {
            "q":self.trans_data,
            "from":self.fromlang,
            "to":self.tolang,
            "appid":self.appid,
            "sign":self.sign,
            "salt":self.salt,
            "domain":self.domain
        }
        get_base = self.session.post(self.url,data=post_data)
        #print(get_base.json())
        return get_base.json()

#a = Trans(appid,secretKey)
#b=a.start_trans("China","zh","medicine")
#print(b)