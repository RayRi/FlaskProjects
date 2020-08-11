#coding:utf8
from __future__ import absolute_import

import os
from flask import Flask, render_template
from logging.config import dictConfig

# 配置 log
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })


def create_app(test_config=None):
    """工厂化函数

    主要作用是创建应用
    """
    app = Flask(__name__, instance_relative_config=True)
    """
    设置一个应用的 缺省配置：
    SECRET_KEY 是被 Flask 和扩展用于保证数据安全的。在开发过程中， 为了方便可以设置为 'dev'，
        但是在发布的时候应当使用一个随机值来 重载它。
    DATABASE SQLite 数据库文件存放在路径。它位于 Flask 用于存放实例的 app.instance_path 
        之内。下一节会更详细 地学习数据库的东西。
    """ 
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "recommendation.sqlite")
    )

    """
    使用 config.py 中的值来重载缺省配置，如果 config.py 存在的话。 例如，当正式部署的时候，
        用于设置一个正式的 SECRET_KEY 。
    test_config 也会被传递给工厂，并且会替代实例配置。这样可以实现 测试和开发的配置分离，相互独立。
    """
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # Flask 不会自动 创建实例文件夹，但是必须确保创建这个文件夹，因为 SQLite 数据库文件会被 保存在里面
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # 首页路由
    @app.route("/hello")
    def index():
        return render_template("base.html")

    # 如果需要处理数据库数据，需要将 databsse.db 模块中内容导入并调用
    from recommendation.database import db
    db.init_app(app)
    
    # 注册蓝图
    from recommendation.scaffolding import cold, collaborate
    app.register_blueprint(cold.bp)

    # 添加蓝图之外，设置一个 url 规则，确保 index 视图会用于 /
    app.register_blueprint(collaborate.bp)
    app.add_url_rule("/", endpoint="index")

    return app