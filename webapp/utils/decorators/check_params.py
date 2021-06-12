"""
检验用于提交的图片数据是否符合遥要求
"""
import json
from functools import wraps
from flask import request, current_app

from webapp.utils.API_RESPONE_CODE import API_RESPONE_CODE


def request_required_params(params_list):
    """检查用于提交的图像是否合乎要求"""
    def request_required_params_decorator(f):
        @wraps(f)
        def decorate_function(*args, **kwargs):
            resp={}
            post_data = request.get_data(as_text=True)
            try:
                post_data_dict = json.loads(post_data)
            except Exception:
                resp['code'] = API_RESPONE_CODE.REQUEST_ARGUMENTS_ERROR
                resp['error'] = post_data+"不是有效的json数据"
                return json.dumps(resp)

            for key in params_list:
                if key not in post_data_dict.keys():
                    resp['code'] = API_RESPONE_CODE.REQUEST_ARGUMENTS_ERROR
                    resp['error'] = key+"是必填参数"
                    return json.dumps(resp)
                else:
                    kwargs[key]=post_data_dict[key]
            return f(*args, **kwargs)
        return decorate_function
    return request_required_params_decorator
