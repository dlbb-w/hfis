#!/usr/bin/env python
# _*_coding:utf-8 _*_

import pandas as pd
import pickle
import os
import sys
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
# print('root_path is:',root_path)
# sys.path.append(sys.path.append(os.path.split(root_path)[0]+"/classification"))
kg_corpus_path = root_path + '/checkpoint/es_corpus/rx_kg_corpus.pkl'
print('kg_corpus_path is:',kg_corpus_path)

class EsCorpus:
    def __init__(self):
        self.kg_corpus = pickle.load(open(kg_corpus_path, "rb"))


    def save_corpus_file(self,file1,file2,save_file):
        key_word_list = []
        sentence_list = []
        sen_label_list = []
        all_dict_list = []
        data1 = pd.read_excel(file1, header=None,
                             names=['label', 'split_data', 'data'])
        data2 = pd.read_excel(file2,header=None,names=['label','sentence'])
        for d1 in data1['label']:
            sen_label_list.append(d1)
        for d2 in data1['data']:
            d2 = str(d2)
            d2_list = d2.split('、')
            key_word_list.append(d2_list)
        for d3 in data2['sentence']:
            sentence_list.append(d3)
        sentence_keyword_dict = dict(zip(sentence_list, key_word_list))
        sentence_label_dict = dict(zip(sentence_list, sen_label_list))
        print('sen_keyword_dict length is:',len(sentence_keyword_dict))
        print('sen_label_dict length is:',len(sentence_label_dict))
        all_dict_list.append(sentence_keyword_dict)
        all_dict_list.append(sentence_label_dict)
        print('all_dict_list length is:',len(all_dict_list))
        pickle.dump(all_dict_list,open(save_file,'wb'))


    def load_file(self,file_path):
        load_data = pickle.load(open(file_path, 'rb'))
        return load_data


    def search_corpus(self,sentence):
        corpus_data = self.kg_corpus
        sentence_keyword_dict = corpus_data[0]
        sentence_label_dict = corpus_data[1]
        new_label_sentence_dict = {}
        for key,value in sentence_keyword_dict.items():
            for word in value:
                if word in sentence:
                    new_label_sentence_dict[key] = sentence_label_dict[key]
        return new_label_sentence_dict


if __name__ == '__main__':
    ec = EsCorpus()
    print(ec.search_corpus('从严落实春节前后疫情防控措施的通告合防'))

