#coding:utf8
from __future__ import absolute_import

import os
import sys
import pandas as pd

sys.path.append("..")
from database.connections import (
    Manipulater, ENGINE, Series, Similarity
)




def read(file, columns):
    """加载需要的数据
    """
    df = pd.read_csv(file)
    
    return df.loc[:, columns]


def load(data, mapping_fields:dict, data_model):
    """保存数据到数据库"""
    dealer = Manipulater()
    with dealer.get_session() as session:
        # Load data rows to write dat
        for index, row in data.iterrows():
            
            item = data_model(**{key:row[value] for key, value in mapping_fields.items()})
            session.add(item)
            session.commit()

            if index % 1000:
                print(f"加载数据完成阶段: {index}")


if __name__ == "__main__":
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
                item = Series(id="%d" % row["id"], title=row["title"], cover=row["cover_page"])
                session.add(item)
                session.commit()

                if index % 1000:
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

                if index % 1000:
                    print(f"加载数据完成阶段: {index}")