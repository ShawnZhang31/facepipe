from re import A
from typing import Text
from cv2 import data
from flask import request
import json

from webapp.utils.decorators import image_required_withkey, request_required_params
from . import api_v1
from facelib.facedetect import FrontFaceDetect
from webapp.utils.API_RESPONE_CODE import API_RESPONE_CODE

@api_v1.route("/", methods=['GET', 'POST'])
def api_v1_index():
    return "hello 468 face landmarks api v1 from cmit"

@api_v1.route("/face/detect", methods=['POST'])
@request_required_params(['image'])
@image_required_withkey('image')
def api_v1_face_detect(*args, **kwargs):
    image = kwargs['image']

    resp={}


    face_detect = FrontFaceDetect()
    try:
        faces = face_detect.detectFace(image)
    except Exception:
        resp['code'] = API_RESPONE_CODE.SERVER_FACEMODULE_ERROR
        resp['error'] = "人脸检测算子计算错误"
        return json.dumps(resp)
    
    resp['code'] = API_RESPONE_CODE.API_RESPONE_SUCCESS
    resp['error'] = None
    resp['faces'] = faces

    return json.dumps(resp)

@api_v1.route("/face/landmark", methods=['POST'])
@request_required_params(['image'])
@image_required_withkey('image')
def api_v1_face_landmark(*args, **kwargs):
    image = kwargs['image']

    resp={}


    face_detect = FrontFaceDetect()
    try:
        landmarks = face_detect.detectFaceLandmarks(image)
    except Exception:
        resp['code'] = API_RESPONE_CODE.SERVER_FACEMODULE_ERROR
        resp['error'] = "人脸检测算子计算错误"
        return json.dumps(resp)
    
    resp['code'] = API_RESPONE_CODE.API_RESPONE_SUCCESS
    resp['error'] = None
    resp['landmarks'] = landmarks

    return json.dumps(resp)


    
    
    # return json.dumps(context)
    # return "face detect"