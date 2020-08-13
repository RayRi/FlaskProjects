#coding:utf8
"""
# 中文情感分析 API
使用了 CNN TEXT 的搭建的模型，包括了数据预处理和情感倾向标签预测两个阶段。传入数据需要解析的
字符串内容。

## 基础路径
```
# 测试环境
https://basepath/api/v1.0/sentiment
```

## 调用说明
### 请求
开发测试阶段，提供单一的 `POST` 请求，因此在传入数据过程中需要将参数放在请求体

#### 参数传输方式
暂未提供 `GET` 相关方法，因此传输过程不需要将请求参数放入 URL 中当 Query String：
`GET https://basepath/api/v1.0/sentiment?text=测试内容`

应当统一使用 `POST` 方法，将数据统一 JSON 格式放在请求体:
```
PUT https://basepath/api/v1.0/sentiment
Content-Type: application/json
{
    "id": xxx, 
    "text": "xxxxxx xxxx"
}
```

### 响应
成功响应的内容包括基本内容：
```
[
    {
        "id": "xxx"
        "label": x
    }
]
```

### 认证
未采用认证机制

### 请求限制
未采用限制

### 错误
使用标准 HTTP 响应状态码表示 API 请求状态

## 情感分析
### 请求文本情感倾向标签
* 操作 POST /sentiment
* 请求体
    * id 可选，字符串
    * text 必填，字符串
* 响应
    200 状态码
    * status 响应状态码，int
    * id 对应请求体中的 id，str
    * text 对应请求体中的 text，str
    * label 情感倾向标签， int
    * description 对倾向性结果描述，str
    * date 收到请求的时间戳，ISO 时间戳
    * cost 运行模型时间消耗秒数，float

    400 状态码
    * status 响应状态码
    * id 对应请求体中的 id
    * description 对结果描述

## 请求示例
```
$ curl -i -H "Content-Type: application/json" -X POST -d  '{"id": 123, "text": "镇江丹徒区一房子白天起火,诚信肥宅精华 0注册 17-6-30\u3000镇江丹徒区一房子白天起火房主大妈还在酣睡丹徒区一处民房大白天起火，房主大妈却还在酣睡当中。好在有人发现险情后及时报警，民警赶到现场后叫醒房主并将火扑灭。\u3000\u300010月6日中午，上党派出所接群众报警称， 上党镇某村的一处民房失火。民警蔡润生、警辅史琦赶到现场后发现，一农户的厢房冒出浓烟，而消防车还未赶到。民警立刻疏散周围群众，并冲入隔壁卧室，发现一位大妈还在睡觉，立刻将她叫醒。大妈看到厢房失火惊慌失措，民警随即安抚其情绪并查看火势。发现火势并不大，民警让大妈找来一个圆桶，用最原始的救火方式，一桶一桶地浇水灭火。经过近10分钟扑救，民警终于将火浇灭。警方事后了解到，当天中午，房主沈大妈在家招待回家团聚的亲朋好友，后来亲戚朋友都出去打牌、钓鱼了，自己就在家睡午觉，没想到隔壁厢房失火。要不是民警及时叫醒她并灭火，后果不堪设想。[ 本帖最后由 诚信肥宅 于 17-10-9 14:05 编辑 ]已有0人打赏"}' http://localhost:5000/api/v1.0/sentiment

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 2578
Server: Werkzeug/1.0.1 Python/3.7.6
Date: Wed, 12 Aug 2020 03:42:31 GMT

{"cost":0.090139,"date":"2020-08-12T11:42:31.610512","description":"123 \u9884\u6d4b\u60c5\u611f\u503e\u5411\u6027: \u8d1f\u5411","id":"123","label":0,"status":200,"text":"\u9547\u6c5f\u4e39\u5f92\u533a\u4e00\u623f\u5b50\u767d\u5929\u8d77\u706b,\u8bda\u4fe1\u80a5\u5b85\u7cbe\u534e 0\u6ce8\u518c 17-6-30\u3000\u9547\u6c5f\u4e39\u5f92\u533a\u4e00\u623f\u5b50\u767d\u5929\u8d77\u706b \u623f\u4e3b\u5927\u5988\u8fd8\u5728\u9163\u7761\u4e39\u5f92\u533a\u4e00\u5904\u6c11\u623f\u5927\u767d\u5929\u8d77\u706b\uff0c\u623f\u4e3b\u5927\u5988\u5374\u8fd8\u5728\u9163\u7761\u5f53\u4e2d\u3002\u597d\u5728\u6709\u4eba\u53d1\u73b0\u9669\u60c5\u540e\u53ca\u65f6\u62a5\u8b66\uff0c\u6c11\u8b66\u8d76\u5230\u73b0\u573a\u540e\u53eb\u9192\u623f\u4e3b\u5e76\u5c06\u706b\u6251\u706d\u3002\u3000\u300010\u67086\u65e5\u4e2d\u5348\uff0c\u4e0a\u515a\u6d3e\u51fa\u6240\u63a5\u7fa4\u4f17\u62a5\u8b66\u79f0\uff0c\u4e0a\u515a\u9547\u67d0\u6751\u7684\u4e00\u5904\u6c11\u623f\u5931\u706b\u3002\u6c11\u8b66\u8521\u6da6\u751f\u3001\u8b66\u8f85\u53f2\u7426\u8d76\u5230\u73b0\u573a\u540e\u53d1\u73b0\uff0c\u4e00\u519c\u6237\u7684\u53a2\u623f\u5192\u51fa\u6d53\u70df\uff0c\u800c\u6d88\u9632\u8f66\u8fd8\u672a\u8d76\u5230\u3002\u6c11\u8b66\u7acb\u523b\u758f\u6563\u5468\u56f4\u7fa4\u4f17\uff0c\u5e76\u51b2\u5165\u9694\u58c1\u5367\u5ba4\uff0c\u53d1\u73b0\u4e00\u4f4d\u5927\u5988\u8fd8\u5728\u7761\u89c9\uff0c\u7acb\u523b\u5c06\u5979\u53eb\u9192\u3002\u5927\u5988\u770b\u5230\u53a2\u623f\u5931\u706b\u60ca\u614c\u5931\u63aa\uff0c\u6c11\u8b66\u968f\u5373\u5b89\u629a\u5176\u60c5\u7eea\u5e76\u67e5\u770b\u706b\u52bf\u3002\u53d1\u73b0\u706b\u52bf\u5e76\u4e0d\u5927\uff0c\u6c11\u8b66\u8ba9\u5927\u5988\u627e\u6765\u4e00\u4e2a\u5706\u6876\uff0c\u7528\u6700\u539f\u59cb\u7684\u6551\u706b\u65b9\u5f0f\uff0c\u4e00\u6876\u4e00\u6876\u5730\u6d47\u6c34\u706d\u706b\u3002\u7ecf\u8fc7\u8fd110\u5206\u949f\u6251\u6551\uff0c\u6c11\u8b66\u7ec8\u4e8e\u5c06\u706b\u6d47\u706d\u3002\u8b66\u65b9\u4e8b\u540e\u4e86\u89e3\u5230\uff0c\u5f53\u5929\u4e2d\u5348\uff0c\u623f\u4e3b\u6c88\u5927\u5988\u5728\u5bb6\u62db\u5f85\u56de\u5bb6\u56e2\u805a\u7684\u4eb2\u670b\u597d\u53cb\uff0c\u540e\u6765\u4eb2\u621a\u670b\u53cb\u90fd\u51fa\u53bb\u6253\u724c\u3001\u9493\u9c7c\u4e86\uff0c\u81ea\u5df1\u5c31\u5728\u5bb6\u7761\u5348\u89c9\uff0c\u6ca1\u60f3\u5230\u9694\u58c1\u53a2\u623f\u5931\u706b\u3002\u8981\u4e0d\u662f\u6c11\u8b66\u53ca\u65f6\u53eb\u9192\u5979\u5e76\u706d\u706b\uff0c\u540e\u679c\u4e0d\u582a\u8bbe\u60f3\u3002[ \u672c\u5e16\u6700\u540e\u7531 \u8bda\u4fe1\u80a5\u5b85 \u4e8e 17-10-9 14:05 \u7f16\u8f91 ]\u5df2\u67090\u4eba\u6253\u8d4f"}
```
"""

import flask
import werkzeug
import functools
import datetime
from flask import request, jsonify, abort, make_response


from .error import bad_request, NoContent
from . import preprocess, predict

app = flask.Flask(__name__)


# 注册请求异常处理
app.register_error_handler(400, bad_request)

# 情感标签映射
label_mapping = {
    0: "负向",
    1: "中性",
    2: "正向"
}

@app.route("/", methods=["GET", "POST"])
def index():
    return "<h1>欢迎使用情感分析模型</h1><p> TextCNN 模型</p>"



@app.route("/api/v1.0/sentiment", methods=["POST"])
def sentiment():
    """情感倾向性分析
    """
    # 收到请求时间
    date = datetime.datetime.now().isoformat()

    if not request.json or "text" not in request.json:
        abort(400)
    

    # 分析情感倾向性标签
    start = datetime.datetime.now()
    
    try:
        label = predict(preprocess(request.json["text"]))
        description = "{id}预测情感倾向性: {label}".format(
                id= "" if not request.json["id"] else f"{request.json['id']} ",
                label= f"{label_mapping[int(label)]}"
            )
        status = 200
        end = datetime.datetime.now()
    except ValueError as err:
        label = 1
        status = 204
        description = "{id} 文本未正常捕获，将情感倾向预测为: {label}".format(
                id= "" if not request.json["id"] else f"{request.json['id']} ",
                label= f"{label_mapping[int(label)]}")

        end = start


    result = {
        "status": status,
        "id": str(request.json["id"]),
        "text": request.json["text"],
        "label": int(label),
        "description": description,
        "date": date,
        "cost": (end - start).total_seconds()
    }

    return jsonify(result), 200



if __name__ == "__main__":
    app.run()