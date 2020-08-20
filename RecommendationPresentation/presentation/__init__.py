#coding:utf8
from __future__ import absolute_import

import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# from datamodel import Series, Similarity, DATABASE
import sys
sys.path.append("..")
from ..core import Series, Similarity, DATABASE_CONFIGURE, DATABASE


# from RecommendationPresentation.core import DATABASE_CONFIGURE



# * database URI information
URI = "mysql+pymysql://{user}{password}@{host}:{port}/{database}?charset={charset}"

password = "" if not DATABASE_CONFIGURE.mysql.get("password") else f':{DATABASE_CONFIGURE.mysql.get("password")}'
URI = URI.format(
    user=DATABASE_CONFIGURE.mysql.get("user"), password=password,
    host=DATABASE_CONFIGURE.mysql.get('host'), port=DATABASE_CONFIGURE.mysql.get("port"),
    charset= DATABASE_CONFIGURE.mysql.get("charset"), database=DATABASE_CONFIGURE.mysql.get("database")
)

# ! debug
import os
import requests
import base64
URI = "sqlite:///" + os.path.join(os.path.dirname(__file__), "../tests/recommendation_test.db")

# * create app
def create_app():
    app = Flask(__name__)

    # SQLAlchemy 配置信息
    app.config["SQLALCHEMY_DATABASE_URI"] = URI
    app.config["SQLALCHEMY_ECHO"] = DATABASE_CONFIGURE.get("SQLALCHEMY", "ECHO", "bool")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = \
        DATABASE_CONFIGURE.get("SQLALCHEMY", "TRACK_MODIFICATIONS")
    DATABASE.init_app(app)


    # 首页路由
    from .scaffolding import index
    app.register_blueprint(index.bp)
    return app


# * Init application
def run(app):
    with app.app_context():
        """
        user = db.User(...)
        db.session.add(user)
        db.session.commit()
        """
        pass