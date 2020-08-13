#coding:utf8
"""
异常状态码处理
"""
from __future__ import absolute_import
from flask import jsonify, make_response, request
from werkzeug.exceptions import HTTPException

class NoContent(HTTPException):
    """*204* ``No Content``

    结束到请求，但是处理结果不符合条件
    """
    code = 204
    description = (
        "The requested URL was not found on the server. If you entered"
        " the URL manually please check your spelling and try again."
    )



def bad_request(error):
    """Bad Request
    
    请求信息错误，例如请求内容的类型错误，导致不能解析文本信息的响应状态是 400 状态
    """
    return jsonify(
        {
            "status": 400,
            "id": request.json["id"] if request.json["id"] else None,
            "description": "请求信息错误"
        }), 400

