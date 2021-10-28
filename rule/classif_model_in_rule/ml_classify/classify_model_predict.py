#!/usr/bin/env python
# _*_coding:utf-8 _*_

import os
import sys
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import pickle
from utils.config import CLASSIFY_MODEL_PATH
from utils.config import CLASSIFY_TFIDF_MODEL_PATH
# from utils.data_process import context_clean
import pandas as pd

class CModel:
    def __init__(self, name):
        self.label()
        self.loaded_vec = pickle.load(open(self.select_tfidf_path(name), "rb"))
        self.load_model(name)



    def select_model_path(self, name):
        return CLASSIFY_MODEL_PATH[name]


    def select_tfidf_path(self, name):
        return CLASSIFY_TFIDF_MODEL_PATH[name]


    def load_model(self, name):
        with open(self.select_model_path(name), 'rb') as f:
            self.choose_model = pickle.load(f)


    def label(self):
        # self.data = pd.read_csv(doc_train_data_dir + INFILE, header=0, error_bad_lines=False)
        # labels = self.data[[LABEL, CATEGORY]].drop_duplicates()[LABEL].values
        # categories = self.data[[LABEL, CATEGORY]].drop_duplicates()[CATEGORY].values
        dict_lable = {0: 'other', 1: '代码', 2: '名称'}
        self.look_up = dict_lable


    def predict(self, input_text):
        # input_text = context_clean(input_text)
        text_tfidf = self.loaded_vec.transform([input_text])
        tfidf_score = text_tfidf[0]
        x = self.choose_model.predict(tfidf_score)[0]
        y = self.look_up
        x = int(x)
        return y[x]


# if __name__ == '__main__':
#      m = CModel('svm')
#      text = '放博有限公司'
#      print(m.predict(text))


