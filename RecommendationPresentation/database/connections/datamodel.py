#coding:utf8
"""
数据表的数据模型
"""
import sqlalchemy
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
    cover = sqlalchemy.Column(sqlalchemy.VARCHAR(500, convert_unicode=True), nullable=True)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())


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