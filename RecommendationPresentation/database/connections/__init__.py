#coding:utf8
from __future__ import absolute_import

import contextlib
import sqlalchemy
from sqlalchemy import orm

from .datamodel import Series, Similarity, Base
from ..conf import configure

# database URI information
URI = "mysql+pymysql://{user}{password}@{host}:{port}/{database}?charset={charset}"

password = "" if not configure.mysql.get("password") else f':{configure.mysql.get("password")}'
URI = URI.format(
    user=configure.mysql.get("user"), password=password,
    host=configure.mysql.get('host'), port=configure.mysql.get("port"),
    charset= configure.mysql.get("charset"), database=configure.mysql.get("database")
)


ENGINE = sqlalchemy.create_engine(URI, echo=True)


class Manipulater(object):
    """
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
        self.Session.configure(bind=ENGINE)
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
            self.Session.configure(bind=args[0])
        elif "bind" in kwargs:
            self.Session.configure(bind=kwargs['bind'])
        else:
            self.Session.configure(bind=ENGINE)

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
