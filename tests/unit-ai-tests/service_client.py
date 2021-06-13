# -*- coding:utf-8 -*-
import requests
import json
import base64
import time
import math
import uuid
import hashlib
from datetime import datetime
import sys



URL = "http://10.252.92.29:9050/api/v1/face/detect"
APPID = "APPID"#需要您的APPID
APPKey = "APPSECERT"#需要您的APPSECERT
AppName = "face468"

def create_header():
	appid = APPID
	appKey = APPKey
	uuid = "52a7bb1fc08841ad9efc76d8ae1ef07b"
	appName = AppName
	for i in range(24 - len(appName)):
		appName += "0"
	capabilityname = appName
	# print(len(capabilityname))
	csid = appid + capabilityname + uuid
	tmp_xServerParam = {
		"appid": appid,
		"csid": csid
	}
	# print(tmp_xServerParam)
	xCurTime = str(int(math.floor(time.time())) + 600)
	print(xCurTime)
	xServerParam = str(base64.b64encode(json.dumps(tmp_xServerParam).encode('utf-8')), encoding="utf8")
	# xServerParam = str(base64.b64encode(json.dumps(tmp_xServerParam).encode('utf-8')))

	# turn to bytes
	xCheckSum = hashlib.md5(bytes(appKey + xCurTime + xServerParam, encoding="utf8")).hexdigest()
	# xCheckSum = hashlib.md5(bytes(appKey + xCurTime + xServerParam)).hexdigest()

	header = {
		"appKey": appKey,
		"X-Server-Param": xServerParam,
		"X-CurTime": xCurTime,
		"X-CheckSum": xCheckSum,
		"content-type": "application/json;charset=utf8"
	}

	return header

headers_1 = create_header()

image_path = sys.path[0]+'/'+'111.png'

with open(image_path, 'rb') as f:
    base64_str = base64.b64encode(f.read())



body = {
			"requestTime": "2018-03-08 15:40:30",
			"appId": "scwsb_app",
            "contain":"xxx",
			"image": str(base64_str)
	   }
json_in = json.dumps(body, ensure_ascii=False)

res_info = requests.post(url=URL, data=json_in,headers =headers_1, timeout=100)
print(res_info.text,res_info.status_code,res_info.headers)
print(res_info.text.encode('utf-8').decode('unicode_escape'))
print(res_info.elapsed.total_seconds())