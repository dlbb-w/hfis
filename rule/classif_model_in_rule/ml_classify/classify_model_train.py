#!/usr/bin/env python
# _*_coding:utf-8 _*_

import os
import sys
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import pickle
from utils.config import CLASSIFY_MODEL_MAPPER
from utils.config import CLASSIFY_MODEL_PATH
from utils.config import CLASSIFY_TFIDF_MODEL_PATH
from utils.config import doc_train_data_dir
from utils.config import DATA,LABEL,CATEGORY,INFILE

class Model:
    def __init__(self, name):
        self.name = name
        self.tfvectorizer()
        self.load_data()
        # self.label()
        self.load_model()


    def train_model(self):
         return CLASSIFY_MODEL_MAPPER[self.name]


    def select_model_path(self):
         return CLASSIFY_MODEL_PATH[self.name]


    def select_tfidf_path(self):
        return CLASSIFY_TFIDF_MODEL_PATH[self.name]



    def load_data(self):
        self.data = pd.read_csv(doc_train_data_dir+INFILE , header=0, error_bad_lines=False)
        articles = np.array(self.data[DATA])
        labels = np.array(self.data[LABEL])
        # articles = pd.get_dummies(articles,drop_first=True)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(articles, labels, test_size=0.3)


    def load_model(self):
        with open(self.select_model_path(), 'rb') as f:
            self.choose_model = pickle.load(f)


    def label(self):
        labels = self.data[[LABEL, CATEGORY]].drop_duplicates()[LABEL].values
        categories = self.data[[LABEL, CATEGORY]].drop_duplicates()[CATEGORY].values
        self.look_up = dict(zip(labels, categories))


    def tfvectorizer(self):
        self.tf_vectorizer = TfidfVectorizer(min_df=1, max_df= 1.0, ngram_range=(1, 2), use_idf=True,analyzer='char')


    def train(self):
        x_train_tfidf = self.tf_vectorizer.fit_transform(self.x_train)
        with open(self.select_tfidf_path(), 'wb') as fw:
            pickle.dump(self.tf_vectorizer, fw)
            print('tfidf model restore success!')
        ts = self.train_model().fit(x_train_tfidf, self.y_train)
        # print(self.x_train)
        # ts = self.train_model().fit(self.x_train, self.y_train)
        with open(self.select_model_path(), 'wb') as f:
            pickle.dump(ts, f)
            print('classification model restore success!')


    def evaluate(self):
        x_test, y_test = self.x_test, self.y_test
        loaded_vec = pickle.load(open(self.select_tfidf_path(), "rb"))
        x_test_tfidf = loaded_vec.transform(x_test)
        predictions =self.choose_model.predict(x_test_tfidf)
        # predictions =self.choose_model.predict(x_test)
        # print(predictions[:100])
        print(classification_report((y_test), predictions))
        print("The accuracy score is {:.2%}".format(accuracy_score(y_test, predictions)))


if __name__ == '__main__':
    m = Model('svm')
    # m.train()
    m.evaluate()

