#coding:utf8
from __future__ import absolute_import


import os

from ..bin.__parser import DatabaseParser
from .datamodel import Series, Similarity, Base

# config file
database_file = os.path.join(os.path.dirname(__file__), "./database.ini")

# database configuration object
DATABASE_CONFIGURE = DatabaseParser(database_file)