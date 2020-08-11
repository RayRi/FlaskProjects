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

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
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
注册蓝图
当用访问 /cold/register URL 时， register 视图会返回用于填写注册 内容的表单的 HTML 。
当用户提交表单时，视图会验证表单内容，然后要么再次 显示表单并显示一个出错信息，
要么创建新用户并显示登录页面。
"""
@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    这个 register 视图做了以下工作：
    1. @bp.route 关联了 URL /register 和 register 视图函数。当 Flask 收到一个指向 
        /cold/register 的请求时就会调用 register 视图并把其返回值作为响应
    2. 如果用户提交了表单，那么 request.method 将会是 'POST' 该情况下会开始验证用户的输入内容。
    3. request.form 是一个特殊类型的 dict ，其映射了提交表单的键和值。表单中，用户将会输入其
         username 和 password 
    4. 验证 username 和 password 不为空
    5. 通过查询数据库，检查是否有查询结果返回来验证 username 是否已被注册。 db.execute 
        使用了带有 ? 占位符 的 SQL 查询语句。占位符可以代替后面的元组参数中相应的值。使用占
        位符的 好处是会自动帮你转义输入值，以抵御 SQL 注入攻击

        fetchone() 根据查询返回一个记录行。 如果查询没有结果，则返回 None 。后面还用到 
            fetchall() ，它返回包括所有结果的列表
    6. 如果验证成功，那么在数据库中插入新用户数据。为了安全原因，不能把密码明文储存在数据库中。
        相代替的，使用 generate_password_hash() 生成安全的哈希值并储存 到数据库中。查询修
        改了数据库是的数据后使用 meth:db.commit() <sqlite3.Connection.commit> 保存修改。
    7. 用户数据保存后将转到登录页面。 url_for() 根据登录视图的名称生成相应的 URL 。与写固定
        的 URL 相比， 这样做的好处是如果以后需要修改该视图相应的 URL ，那么不用修改所有涉及到
         URL 的代码。 redirect() 为生成的 URL 生成一个重定向响应
    8. 如果验证失败，那么会向用户显示一个出错信息。 flash() 用于储存在渲染模块时可以调用的信息
    9. 当用户最初访问 cold/register 时，或者注册出错时，应用显示一个注册 表单
        render_template() 会渲染一个包含 HTML 的模板。你会在教程的下一节 学习如何写这个模板
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "username required"
        elif not password:
            error = "password required"
        elif db.execute(
            "SELECT id FROM user WHERE username=?", (username, )
        ).fetchone() is not None:
            error = f"username {username} is already registered"

        if error is None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)", 
                (username, generate_password_hash(password))
            )

            # 提交数据
            db.commit()

            return redirect(url_for("cold.login"))
        else:
            flash(error)
    # 非提交页面和提交信息错误，都定向到注册页面
    return render_template("cold/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    与 register 有以下不同之处：
    1. 首先需要查询用户并存放在变量中，以备后用
    2. check_password_hash() 以相同的方式哈希提交的 密码并安全的比较哈希值。如果匹配成功，
        那么密码就是正确的
    3. session 是一个 dict ，它用于储存横跨请求的值。当验证 成功后，用户的 id 被储存于一个
        新的会话中。会话数据被储存到一个 向浏览器发送的 cookie 中，在后继请求中，浏览器会返
        回它。 Flask 会安全对数据进行签名以防数据被篡改
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username=?", (username, )
        ).fetchone()

        if user is None:
            error = "incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]

            return redirect(url_for("index"))
        else:
            flash(error)

    return render_template("cold/login.html")


"""
在用户 id 已经存储的情况，后续的请求中应该是可以直接调用该信息的。每个请求的开头，如果用户已登录，
那么其用户信息应当被载入，以使其可用于其他视图
"""
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id=?", (user_id, )
        ).fetchone()


"""注销
注销的时候需要把用户 id 从 session 中移除。 然后 load_logged_in_user 就不会在后继请求中
载入用户了
"""
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


"""
解决必要登录才能进行的相关的操作，例如创建、编辑以及删除博客等处理。
这里的操作使用装饰器完成：
装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。新的函数检查用户 是否已载入。如果已载
    入，那么就继续正常执行原视图，否则就重定向到登录页面。 我们会在博客视图中使用这个装饰器。

需要注意蓝图和视图的端点，在 url_for 函数中使用有差异：

url_for() 函数根据视图名称和发生成 URL 。视图相关联的名称亦称为 端点 ，缺省情况下，端点名称与
    视图函数名称相同。
例如，前文被加入应用工厂的 hello() 视图端点为 'hello' ，可以使用 url_for('hello') 来连接。
    如果视图有参数，后文会看到，那么可使用 url_for('hello', who='World') 连接。

当使用蓝图的时候，蓝图的名称会添加到函数名称的前面。上面的 login 函数 的端点为 'cold.login'，
    因为它已被加入 'cold' 蓝图中。
"""
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('cold.login'))

        return view(**kwargs)

    return wrapped_view