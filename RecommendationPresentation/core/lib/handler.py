#coding:utf8
from __future__ import absolute_import

import contextlib
import sqlalchemy
from sqlalchemy import orm

from ..etc import Base, DATABASE_CONFIGURE


# database URI information
URI = "mysql+pymysql://{user}{password}@{host}:{port}/{database}?charset={charset}"

password = "" if not DATABASE_CONFIGURE.mysql.get("password") else f':{DATABASE_CONFIGURE.mysql.get("password")}'
URI = URI.format(
    user=DATABASE_CONFIGURE.mysql.get("user"), password=password,
    host=DATABASE_CONFIGURE.mysql.get('host'), port=DATABASE_CONFIGURE.mysql.get("port"),
    charset= DATABASE_CONFIGURE.mysql.get("charset"), database=DATABASE_CONFIGURE.mysql.get("database")
)


ENGINE = sqlalchemy.create_engine(URI, echo=True)


class Manipulater(object):
    """使用 SQLAlchemy 操作数据
    操作数据:
    1. 写入数据
    2. 查询数据
    """
    def __new__(cls):
        instance = super(Manipulater, cls).__new__(cls)
        instance.Session = sqlalchemy.orm.sessionmaker()
        
        return instance


    def __init__(self):
        # create table, pass `checkfirst=True`, so that enforce check existence 
        # before create table
        Base.metadata.create_all(ENGINE, checkfirst=True)


    def __enter__(self):
        self.Session.DATABASE_CONFIGURE(bind=ENGINE)
        self.__session = self.Session()
        return self.__session


    def __exit__(self, type, value, traceback):
        self.Session.kw["bind"] = None
        self.__session.close()
        return True

    
    @contextlib.contextmanager
    def get_session(self, *args, **kwargs):
        """session 上下文管理方法

        session 对象，用于对数据操作。在开始前会绑定一个 ENGINE，接受自定义的 engine。第一
        个默认的位置参数优先作为 engine，或者接受一个 bind 的关键字参数
        """
        # check whether engine binded, if there is not engine,
        if len(args) >= 1:
            self.Session.DATABASE_CONFIGURE(bind=args[0])
        elif "bind" in kwargs:
            self.Session.DATABASE_CONFIGURE(bind=kwargs['bind'])
        else:
            self.Session.DATABASE_CONFIGURE(bind=ENGINE)

        # 创建 session 对象
        session = self.Session()

        try:
            yield session
        except sqlalchemy.exc.StatementError as error:
            session.rollback()
            raise sqlalchemy.exc.StatementError(error)
        finally:
            # recover engine is None
            self.Session.kw["bind"] = None
            session.close()
