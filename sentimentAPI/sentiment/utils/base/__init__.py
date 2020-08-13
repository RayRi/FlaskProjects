#-*-coding:utf8-*-
"""
Load some basic words material:
SENTIMENT_WORDS: It's Boson Sentiment dict and negative word. It's used to add
    Jieba dict
STOPWORDS: It's Baidu Stopwords
WHOLE_WIDTH_DICT: It's a whole width mapping
"""
from __future__ import absolute_import

import os
from .__load_data import _load_file, _load_from_path, _load_mapping_data

__all__ = ["_load_file", "_load_from_path", "SENTIMENT_WORDS", "STOPWORDS", "WHOLE_WIDTH_DICT"]

__current_path = os.path.dirname(__file__)

# Load Boson sentiment word and negative word
SENTIMENT_WORDS = _load_from_path(os.path.join(__current_path, "SentimentDict"), \
    extension="txt", mapping=False)

# Load Stopwords
STOPWORDS = _load_from_path(os.path.join(__current_path, "StopWords"), "txt")


# Load whole width mapping
WHOLE_WIDTH_DICT = _load_from_path(os.path.join(__current_path, \
    "Appendix"), extension="txt", mapping=True)


