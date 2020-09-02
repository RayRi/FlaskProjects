#coding:utf8
from __future__ import absolute_import

import os
import pandas as pd
import requests
import base64
import contextlib 
import sqlalchemy 
from sqlalchemy import orm 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import func   




# declarative Base
Base = declarative_base()

class Series(Base):
    """影视数据表"""
    __tablename__ = "series"

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, autoincrement=True)
    series_id = sqlalchemy.Column(sqlalchemy.VARCHAR(20, convert_unicode=True), nullable=False)
    title = sqlalchemy.Column(sqlalchemy.VARCHAR(length=150, convert_unicode=True), nullable=False)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    # 保存原始 URL 的字段设置
    # cover = sqlalchemy.Column(sqlalchemy.VARCHAR(500, convert_unicode=True), nullable=True)

    # 保存为 BLOB 数据在字段甚至
    cover = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)


    def __repr__(self):
        format = "<%s data model object at %s>"
        return format % (self.__class__.__name__, hex(id(self)))

    
    def __str__(self):
        format_ = "<{name}(id='{id}', series_id='{series_id}', title=" + \
            "'{title}', cover='{cover}', create_time='{create_time}')>"
        items = {key: self.__getattribute__(key) for key in self.__dir__() \
            if not key.startswith("_")}

        return format_.format(name=self.__tablename__, **items)



class Similarity(Base):
    """相似度表"""
    __tablename__ = "similarity"

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, autoincrement=True)
    sid1 = sqlalchemy.Column(sqlalchemy.VARCHAR(20), nullable=False, comment="影视 ID")
    sid2 = sqlalchemy.Column(sqlalchemy.VARCHAR(20), nullable=False, comment="影视 ID")
    sim = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=False, default=0, comment="相似度")

    def __repr__(self):
        format = "<%s data model object at %s>"
        return format % (self.__class__.__name__, hex(id(self)))

    
    def __str__(self):
        format_ = "<{name}(id='{id}', sid1='{sid1}', sid2='{sid2}', sim='{sim}')>"
        items = {key: self.__getattribute__(key) for key in self.__dir__() \
            if not key.startswith("_")}

        return format_.format(name=self.__tablename__, **items)


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


def read(file, columns):
    """加载需要的数据
    """
    df = pd.read_csv(file)
    
    return df.loc[:, columns]



if __name__ == "__main__":
    URI = "sqlite:///recommendation_test.db" 
    ENGINE = sqlalchemy.create_engine(URI, echo=True)
    dealer = Manipulater()

    print("读取和保存数据:")
    # 处理影视条目数据
    if False:
        douban_file = os.path.join(os.path.dirname(__file__), "./douban.csv")
        columns = ["id", "title", "cover_page"]
        data = read(douban_file, columns)
        with dealer.get_session() as session:
            # Load data rows to write dat
            for index, row in data.iterrows():
                item = Series(series_id="%d" % row["id"], title=row["title"], cover=row["cover_page"])
                session.add(item)
                session.commit()

                if index % 1000 == 0:
                    print(f"加载数据完成阶段: {index}")

    # 处理相似度结果数据
    if True:
        similarity_file = os.path.join(os.path.dirname(__file__), "./similarities.csv")
        columns = ["id1","id2", "dotProduct"]

        data = read(similarity_file, columns)
        
        with dealer.get_session() as session:
            # Load data rows to write dat
            for index, row in data.iterrows():
                item = Similarity(sid1="%d" % row["id1"], sid2="%d" % row["id2"], sim=float(row["dotProduct"]))
                session.add(item)
                session.commit()

                if index % 1000 == 0:
                    print(f"加载数据完成阶段: {index}")