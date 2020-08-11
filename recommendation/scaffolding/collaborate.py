#coding:utf8

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from recommendation.scaffolding.cold import login_required
from recommendation.database.db import get_db

"""
注意这里，没有设置 predix_url。在 app 中注册蓝图时，还会添加 url 规则，确保 index 的视图
是会用于 /

index 视图的端点会被定义为 collaborate.index 。一些验证视图 会指定向普通的 index 端点。 
使用 app.add_url_rule() 关联端点名称 'index' 和 /  ，这样 url_for('index') 或 
url_for('collaborate.index') 都会有效，会生成同样的 / 链接。

在某些应用，如果工厂中给博客蓝图一个 url_prefix 并定义一个独立的 index 视图，类似前文 cold 中的 
hello 视图。在这种情况下 index 和 collaborate.index 的端点和 URL 会有所不同
"""
# 因为建立的骨架是使用 index.html，这里的方案还是需要设置一个 url_prefix
bp = Blueprint("collaborate", __name__)
# bp = Blueprint("collaborate", __name__, url_prefix="/collaborate")


"""
索引
索引会显示所有帖子，最新的会排在最前面。为了在结果中包含 user 表中的 作者信息，使用了一个 JOIN 
"""

@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username "
            " FROM post p JOIN user u ON p.author_id = u.id"
            " ORDER BY created DESC"
    ).fetchall()
    # import ipdb; ipdb.set_trace()
    return render_template("collaborate/index.html", posts=posts)


"""
创建
create 视图与 register 视图原理相同。要么显示表单，要么发送内容已通过验证且内容已加入数据库，
    或者显示一个出错信息。

先前写的 login_required 装饰器用在了博客视图中，这样用户必须登录以后 才能访问这些视图，否则
    会被重定向到登录页面。
"""
@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "title is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?,?,?)",
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('collaborate.index'))
    return render_template("collaborate/create.html")

"""
更新
update 和 delete 视图都需要通过 id 来获取一个 post ，并且检查作者与登录用户是否一致。为避免
    重复代码，可以写一个函数来获取 post, 并在每个视图中调用它。

abort() 会引发一个特殊的异常，返回一个 HTTP 状态码。它有一个可选参数， 用于显示出错信息，
    若不使用该参数则返回缺省出错信息。 404 表示“未找到”，403 代表“禁止访问”。（ 401 表示
    “未授权”，但是我们重定向到登录 页面来代替返回这个状态码）

check_author 参数的作用是函数可以用于在不检查作者的情况下获取一个 post 。这主要用于显示一个
    独立的帖子页面的情况，因为这时用户是谁没有关系， 用户不会修改帖子
"""

def get_post(id, check_author=True):
    post = get_db().execute(
        "SELECT p.id, title, body, created, author_id, username "
        "FROM post p JOIN user u ON p.author_id = u.id "
        "WHERE p.id=?", (id, )
    ).fetchone()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist")
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not tile:
            error = "title is required"
        
        if error is not None:
            flash(error)
        else:
            db = get_db().execute(
                "UPDATE post set tile=?, body=? WHERE id=?", (title, body, id)
            )

            db.commit()
            return redirect(url_for("collaborate.index"))

    return render_template("collaborate/update.html", post=post)


"""
删除
删除视图没有自己的模板。删除按钮已包含于 update.html 之中，该按钮指向 /<id>/delete URL 。
既然没有模板，该视图只处理 POST 方法并重定向到 index 视图。
"""

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('collaborate.index'))