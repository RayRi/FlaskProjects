#coding:utf8
"""
蓝图和视图
视图是一个应用对请求进行响应的函数。 Flask 通过模型把进来的请求 URL 匹配到 对应的处理视图。
视图返回数据， Flask 把数据变成出去的响应。 Flask 也可以反 过来，根据视图的名称和参数生成 URL 。

创建蓝图
Blueprint 是一种组织一组相关视图及其他代码的方式。与把视图及其他 代码直接注册到应用的方式不同，
蓝图方式是把它们注册到蓝图，然后在工厂函数中 把蓝图注册到应用。

蓝图非常棒的作用是能有效组织和管理需要的模块。例如对于博客管理需要认证才能访问帖子，所以认证和帖子
访问进行分开管理，例如 templates 中 cold 和 blog 模块
"""
import functools
import numpy as np
from RecommendationPresentation.core import Series, Similarity
from flask_sqlalchemy import sqlalchemy
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from recommendation.database.db import get_db


"""
这里创建了一个名称为 'cold' 的 Blueprint 。和应用对象一样， 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 
url_prefix 会添加到所有与该蓝图关联的 URL 前面

在使用之前，需要 app.register_blueprint() 导入并注册蓝图
"""
bp = Blueprint("cold", __name__, url_prefix="/cold")


"""
请求基于内容标签的冷启动
"""
@bp.route("/", methods=["GET"])
def initial():
    error = None
    # 获取随机的 12 个数据，表示用户待播放序列
    ids = np.random.choice(np.arange(1, len(Series.query.all())), 12)
    watching_series = Series.query.filter(Series.id.in_(ids.tolist())).all()

    # 判断是否获取到信息
    if not watching_series:
        # abort(404, Response("<h1>没有请求到资源</h1>"))
        # debug
        abort(Response("<h1>没有请求到资源</h1>"))

    for item in watching_series:
        item.cover = item.cover.decode("ascii") if item.cover else None

    return render_template("cold/index.html", series=watching_series)


"""
根据待播放序列的点击行为请求新数据
"""
@bp.route("/recommend", methods=["POST", "GET"])
def recommendations():
    error = None
    # 获取请求的 id
    
    id_ = request.form.get("series_id", type=str)
    
    if not id_:
        error = "数据发送不正确"
    
    # 请求数据正确，那么 error 为 None
    if error is None:
        datum = Similarity.query.filter(Similarity.sid1==id_) \
                .order_by(sqlalchemy.desc(Similarity.sim)).limit(36)

        # 为了数据呈现数据排序依据，保留了相似性数据值
        result = []
        for data in datum:
            item = Series.query.filter(Series.series_id== data.sid2).first()
            
            temp = {}
            temp["title"] = item.title
            temp["similarity"] = data.sim
            temp["cover"] = item.cover.decode("ascii") if item.cover else None
            temp['series_id'] = item.series_id
            
            result.append(temp)
        # import ipdb; ipdb.set_trace()
        return jsonify(result=result), 200
    else:
        return jsonify(result=["没有获取到推荐条目"]), 200
    

