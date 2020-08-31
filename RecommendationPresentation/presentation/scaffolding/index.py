#coding:utf8
"""
展示页面首页蓝图：
1. 解决展示 10 条内容作为 Top10 的内容
2. 解决以 Top10 内容为条目的推荐
"""
from __future__ import absolute_import

import numpy as np
from collections import Counter
from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, abort,
    Response
)

from RecommendationPresentation.core import Series, Similarity

# 注册首页蓝图
bp = Blueprint("index", __name__)

@bp.route("/", methods=["GET"])
def home():
    """首页视图
    """
    error = None
    # 获取随机的 10 个数据
    ids = np.random.choice(np.arange(1, len(Series.query.all())), 10)
    
    series = Series.query.filter(Series.id.in_(ids.tolist())).all()
    # for item in series:
    #     item.cover = item.cover.decode("ascii")

    # 判断是否获取到信息
    if not series:
        # abort(404, Response("<h1>没有请求到资源</h1>"))
        # debug
        abort(Response("<h1>没有请求到资源</h1>"))

    # 解析 10 个备选数据中对应的推荐条目
    # 采用的依据是：对所有条目计数，从高到低排序
    series_ids = [item.series_id for item in series]
    recommendation_most = Counter([item.sid2 for sid1 in series_ids \
        for item in Similarity.query.filter(Similarity.sid1 == sid1).all()]).most_common(24)
    
    recommendation_ids = [item[0] for item in recommendation_most]
    recommendations = [] 

    for id_, count in recommendation_most:
        item = Series.query.filter(Series.series_id == id_).first()
        item.count = count
        recommendations.append(item)
        item.cover = item.cover.decode("ascii") if item.cover else None

    return render_template("index.html", series=series, recommendations=recommendations)
