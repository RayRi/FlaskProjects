#coding:utf8
"""
解析配置信息
"""
import os
import configparser
import abc


class Parser(metaclass=abc.ABCMeta):
    def read(self, filename):
        """解析出配置信息

        解析指定文件中的配置信息
        """
        NotImplemented


    def get(self, section, option, type=None):
        """提取特定的配置信息

        通过申明 option 和 section 的配置信息，并且可以通过 type 表示需要提取的配置数据类型

        Args:
        --------
        section: str, 配置信息中的 section 名称
        option: str, 在 section 配置下的 option 对应的值
        type: str, 获取的数据类型，默认为 None，即没有申明特定的数据类型；`int` 表示提取的
            数据值为 int，`float` 表示提取数据为 float，`bool` 或者 `boolean` 表示提取
            的数据类型为布尔型数据
        """
        NotImplemented
        


    def check_section(self, section):
        """检测 section

        检查 section 是否存在
        """
        NotImplemented




class DatabaseParser(Parser):
    def __init__(self, filename):
        # create parser object
        self.parser = configparser.ConfigParser()
        self.read(filename)


    def read(self, filename):
        """解析出配置信息

        解析指定文件中的配置信息
        """
        # check file existed
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} doesn't exist")

        self.parser.read(filename)


    def get(self, section, option, type=None):
        """提取特定的配置信息

        通过申明 option 和 section 的配置信息，并且可以通过 type 表示需要提取的配置数据类型

        Args:
        --------
        section: str, 配置信息中的 section 名称
        option: str, 在 section 配置下的 option 对应的值
        type: str, 获取的数据类型，默认为 None，即没有申明特定的数据类型；`int` 表示提取的
            数据值为 int，`float` 表示提取数据为 float，`bool` 或者 `boolean` 表示提取
            的数据类型为布尔型数据
        """
        self.check_section(section)

        if type.lower() == "int":
            return self.parser.getint(section, option)
        elif type.lower() == "float":
            return self.parser.getfloat(section, option)
        elif type.lower() in ["bool", "boolean"]:
            return self.parser.getboolean(section, option)
        else:
            return self.parser.get(section, option)



    @property
    def mysql(self):
        """MySQL 全局配置信息
        """
        self.check_section("mysql")

        config = {key: self.parser.get("mysql", key) for key in \
            self.parser.options("mysql")}
        
        return config


    @mysql.setter
    def mysql(self, key, value):
        """MySQL 配置信息设置

        不允许修改原始配置信息
        """
        NotImplemented
    


    @property
    def sqlalchemy(self):
        """SQLAlchemy 全局配置信息
        """
        self.check_section("SQLALCHEMY")
        
        config = {key: self.parser.get("SQLALCHEMY", key) for key in \
            self.parser.options("SQLALCHEMY")}
        
        return config


    @sqlalchemy.setter
    def sqlalchemy(self, key, value):
        """SQLAlchemy 配置信息设置

        不允许修改原始配置信息
        """
        NotImplemented 


    def check_section(self, section):
        """检测 section

        检查 section 是否存在
        """
        if not self.parser.has_section(section):
            raise LookupError(f"There is not {section} Secton in configuration")
        else:
            pass
