#!/usr/bin/env python
# coding: utf-8

from gensim.summarization import summarize
import re
import pandas as pd

def do_abstract(text):
    text = re.sub(r'。', '. ', text)  # |？|！
    abstract = summarize(text, ratio=0.1)
    return abstract

data = pd.read_excel('../te_data.xlsx')
data = data['知识内容']
text = data[700]
print(text)
extract = do_abstract(text)
print(' ')
print('提取：', extract)