#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于进行http请求，以及MD5加密，生成签名的工具类

import httplib
import urllib
import json
import hashlib
import time

def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    return  hashlib.md5(sign+'secret_key='+secretKey).hexdigest().upper()

def httpGet(url,resource,params=''):
    conn = httplib.HTTPSConnection(url, timeout=10)
    conn.request("GET",resource + '?' + params)
    response = conn.getresponse()
    data = json.load(response)
    return data

def httpPost(url,resource,params):
     headers = {
            "Content-type" : "application/x-www-form-urlencoded",
     }
     conn = httplib.HTTPSConnection(url, timeout=10)
     temp_params = urllib.urlencode(params)
     conn.request("POST", resource, temp_params, headers)
     response = conn.getresponse()
     data = json.load(response)
     params.clear()
     conn.close()
     return data


        
     
