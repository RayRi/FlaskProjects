#coding:utf8
"""
展示页面首页蓝图：
1. 解决展示 10 条内容作为 Top10 的内容
2. 解决以 Top10 内容为条目的推荐
"""
from __future__ import absolute_import

import numpy as np

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
    ids = np.random.randint(1, len(Series.query.all()), 10)
    series = Series.query.filter(Series.id.in_(ids.tolist())).all()

    # 判断是否获取到信息
    if not series:
        abort(404, Response("没有请求到资源"))

    # 解析 10 个备选数据中对应的推荐条目
    # 采用的依据是：对所有条目计数，从高到低排序
    return render_template("index.html", series=series)
