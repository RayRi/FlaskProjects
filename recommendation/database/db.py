#coding:utf8
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

"""
g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存 可能多个函数都会用到的数据。
    把连接储存于其中，可以多次使用，而不用在同一个 请求中每次调用 get_db 时都创建一个新的连接。

current_app 是另一个特殊对象，该对象指向处理请求的 Flask 应用。这里 使用了应用工厂，
那么在其余的代码中就不会出现应用对象。当应用创建后，在处理 一个请求时， get_db 会被调用。
这样就需要使用 current_app 

sqlite3.Row 告诉连接返回类似于字典的行，这样可以通过列名称来操作 数据
"""

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """关闭数据库"""
    db = g.pop("db", None)

    if db is not None:
        db.close()


"""
open_resource() 打开一个文件，该文件名是相对于 flaskr 包的。这样就不需要考虑以后应用具体部署
    在哪个位置。 get_db 返回一个数据库连接，用于执行文件中的命令

click.command() 定义一个名为 init-db 命令行，它调用 init_db 函数，并为用户显示一个成功的
    消息。 更多关于如何写命令行的内容请参阅 ref:cli 

"""

def init_db():
    db = get_db()

    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


"""
close_db 和 init_db_command 函数需要在应用实例中注册，否则无法使用。 然而，既然我们使用了工厂函数，那么在写函数的时候应用实例还无法使用。
    代替地， 我们写一个函数，把应用作为参数，在函数中进行注册。

app.teardown_appcontext() 告诉 Flask 在返回响应后进行清理的时候调用此函数。

app.cli.add_command() 添加一个新的 可以与 flask 一起工作的命令。

在工厂中导入并调用这个函数。在工厂函数中把新的代码放到 函数的尾部，返回应用代码的前面

之后可以直接使用 flask init-db 激活数据库，得到结果会在 instance 文件夹中创建
"""
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)