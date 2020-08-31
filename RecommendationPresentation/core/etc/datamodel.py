#coding:utf8
"""
数据表的数据模型
"""
from __future__ import absolute_import
import datetime
from flask_sqlalchemy import SQLAlchemy


DATABASE = SQLAlchemy(session_options={"autoflush": False})


class Series(DATABASE.Model):
    """影视数据表"""
    __tablename__ = "series"

    id = DATABASE.Column(DATABASE.BigInteger, primary_key=True, autoincrement=True)
    series_id = DATABASE.Column(DATABASE.VARCHAR(20, convert_unicode=True), nullable=False)
    title = DATABASE.Column(DATABASE.VARCHAR(length=150, convert_unicode=True), nullable=False)
    cover = DATABASE.Column(DATABASE.VARCHAR(500, convert_unicode=True), nullable=True)
    create_time = DATABASE.Column(DATABASE.DateTime, default=datetime.datetime.utcnow())


    def __repr__(self):
        format = "<%s data model object at %s>"
        return format % (self.__class__.__name__, hex(id(self)))

    
    def __str__(self):
        format_ = "<{name}(id='{id}', series_id='{series_id}', title=" + \
            "'{title}', cover='{cover}', create_time='{create_time}')>"
        items = {key: self.__getattribute__(key) for key in self.__dir__() \
            if not key.startswith("_")}

        return format_.format(name=self.__tablename__, **items)

    
    def __eq__(self, other):
        """比较两个对象是不是相等
        """
        return self.series_id == other.series_id



class Similarity(DATABASE.Model):
    """相似度表"""
    __tablename__ = "similarity"

    id = DATABASE.Column(DATABASE.BigInteger, primary_key=True, autoincrement=True)
    sid1 = DATABASE.Column(DATABASE.VARCHAR(20), nullable=False, comment="影视 ID")
    sid2 = DATABASE.Column(DATABASE.VARCHAR(20), nullable=False, comment="影视 ID")
    sim = DATABASE.Column(DATABASE.FLOAT, nullable=False, default=0, comment="相似度")


    def __repr__(self):
        format = "<%s data model object at %s>"
        return format % (self.__class__.__name__, hex(id(self)))

    
    def __str__(self):
        format_ = "<{name}(id='{id}', sid1='{sid1}', sid2='{sid2}', sim='{sim}')>"
        items = {key: self.__getattribute__(key) for key in self.__dir__() \
            if not key.startswith("_")}

        return format_.format(name=self.__tablename__, **items)


    
    def __eq__(self, other):
        """比较是否相等
        """
        return self.id == other.id
