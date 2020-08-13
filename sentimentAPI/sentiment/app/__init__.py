#coding:utf8
from __future__ import absolute_import

from sentimentAPI.sentiment.utils.preprocess import feature_extraction
from bs4 import BeautifulSoup

import joblib
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models, layers, preprocessing, Input, metrics



processor = feature_extraction.SentenceProcess()
segmentor = feature_extraction.ExtractToken.init_segmentor(cut_all=False)

# 加载模型信息
tokenizer = joblib.load(os.path.join(os.path.dirname(__file__), \
    "../models/tokenizer_all_data_2e5.pkl"))
model = keras.models.load_model(os.path.join(os.path.dirname(__file__), \
    "../models/full_data_cnn_model.h5"))


def preprocess(text):
    """
    预测情感倾向前的数据处理
    """
    # 处理 HTML 标签
    text = BeautifulSoup(text, "lxml").get_text()

    # 对内容处理
    text = processor.process_pipeline(text, map_char=True)

    # 得到分词结果，并且结果统一使用空格分隔
    return " ".join(segmentor.get_tokens(text, del_cn_punct=True))


def predict(tokens):
    """
    对已经预处理过的文本内容进行预测，得到的每个类别的 Sigmoid 值（需要注意没有使用 softmax 
    处理)

    Args:
    ---------
    tokens: 完成预处理的文本，每个 token 使用空格分隔。可以通过调用 preprocess 处理文本完成
        tokens 的获取
    
    Results:
    ---------
    result: 返回最大值索引，不同的数字值标签表示不同的倾向，0 表示负向，1 表示中性，2 表示正向
    """
    # 如果是字符串数据，那么需要转换为列表
    if isinstance(tokens, str):
        tokens = [tokens]
        
    prediction = model.predict(tokenizer.texts_to_sequences(tokens))
    return prediction.argmax()