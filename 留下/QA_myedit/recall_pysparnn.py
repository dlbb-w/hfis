"""
法律知识问答机器人
通过pysparnn对数据进行召回，得到粗排结果，返回查询问题的答案和其他相似问题
author：王奕朦
date：2021.10.28
"""
import json
import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
root_path = os.path.split(root_path)[0]
print(root_path)
sys.path.append(root_path)
import math
import pickle
import pandas as pd
import time
import config
import pysparnn.cluster_index as ci
from src.recall.sentence2vec import SentenceVectorizer
from shiduAPI import api

sen_vec = SentenceVectorizer()

class Recall_PySparNN:
    def __init__(self, recall_by="sum_avg"):
        self.root_path = config.root_path
        self.recall_by = recall_by
        self.cp_avg_path = os.path.join(self.root_path, "model/recall/cp_sum_avg_HF.pkl")
        files_path = os.path.join(self.root_path, "train/database.json")
        with open(files_path, encoding='utf-8') as f:
            self.dict_data = json.load(f) # 根据database.json生成的字典数据

        # 加载保存到本地的句子向量
        if recall_by == "sum_avg":
            # 如果存在cp，则加载
            if os.path.exists(self.cp_avg_path):
                self.cp = pickle.load(open(self.cp_avg_path, "rb"))
            # 如果不存在，则创建
            else: # TODO 后期应该从数据库中读取
                files_path = os.path.join(self.root_path, "train/database.json")
                self.cp = self.build_cp(files_path)


    def insert(self, sentence):
        """
        函数说明：输入插入
        :param sentence:工单内容，即新问题关键词
        :return:
        """ 
        update_data = api() # 先对sentence进行api
        insert_q = update_data.insert_data(sentence, 0) # 变量解释:（’需api的database.json‘，是否执行）## 0表示执行，改成其他数字则不执行
        for q2_id, q2_content in insert_q.items():
            q2_q, q2_a = list(q2_content.items())[0]
            vector = sen_vec.get_sentence_vector(q2_q) 
            id_sentence = str(q2_id) + "@@@" + ''  # + "@@@" + q2_q.strip()/q2_a.strip()
            # print(q2_q, q2_a, vector)
            self.cp.insert(vector, id_sentence) # 再将api到的sentence加入cp文件

    def dump_cp(self):
        """
        函数说明，定期保存cp文件，防止丢失
        """
        pickle.dump(self.cp, open(self.cp_avg_path, "wb"))


    def build_cp(self):
        """
        函数说明：构建pysparnn所需要的cp文件
        parame：data：DataFrame数据类型的对象（由database.json转换得到）
        return: cp文件
        """
        id_sentence_list = [] # 存放id和文本拼接后的内容
        vector_list = [] # 存放向量
        data = self.get_df_data()
        for index, row in data.iterrows():
            idx = row["idx"]; question = row["question"]; answer = row["answer"]
            # 处理空数据
            if type(question) == float:
                if math.isna(question):
                    continue
            vector = sen_vec.get_sentence_vector(question)  # 获取关键词的向量
            vector_list.append(vector)
            print(vector_list.shape)
            id_sentence_list.append(str(idx)+ "@@@" + '') # + "@@@" + answer.strip()/question.strip() 用answer和question比较慢
        # 构建 cluster_index文件
        cp = ci.MultiClusterIndex(vector_list, id_sentence_list)
        pickle.dump(cp, open(self.cp_avg_path, "wb"))
        return cp


    def get_df_data(self):
        """
        函数说明：根据字典格式的数据库self.dict_data，生成用于构建cp的DataFrame表
        :param：self.dict_data: 读取的json数据文件，是字典格式的数据库
        :return: DataFrame数据类型的对象，3个索引："idx"，"question"， "answer"
        """
        q2_id_l=[]; q2_q_l=[]; q2_a_l = []
        for q1_content in list(self.dict_data.values()):
            for q2_id, q2_content in list(q1_content.values())[0].items():
                q2_q, q2_a = list(q2_content.items())[0]
                q2_id_l.append(q2_id); q2_q_l.append(q2_q); q2_a_l.append(q2_a)
        data = pd.DataFrame({"idx":q2_id_l, "question":q2_q_l, "answer":q2_a_l})
        return data

    def a_simqs(self, q2_id):
        """
        函数说明：根据search到的最相似问题的id，返回答案和其他相似问题列表
        :param q2_id: search到的最相似问题的id
        :return: str类型的答案，和list类型的其他相似问题
        """
        q1_id = q2_id[:3]; simqs = []
        for q1_content in list(self.dict_data[q1_id].values()): 
            for q2_id_i in list(q1_content.keys()):
                if q2_id_i != q2_id:
                    simqs.append(list(q1_content[q2_id_i].keys())[0]) # 其他相似问题 
                else:
                    answer = list(q1_content[q2_id_i].keys())[0] + '@@@' + list(q1_content[q2_id].values())[0] # 最相似问题的答案
        return answer, simqs  

    def search(self, sentence, k=1, k_clusters=10, return_distance=False, recall_by="sum_avg"):
        """
        函数说明：实现快速近邻搜索
        :param sentence: 所需要搜索的问题，str
        :param k: 想要返回相似度最高的问题的个数，int
        :param k_clusters: 所需要聚类的个数 int
        :param return_distance: 是否需要返回距离 True or False
        :return: 答案，和相似问题的df表格
        """
        if recall_by=="sum_avg":
            vector = sen_vec.get_sentence_vector(sentence)
            bt = time.time()
            results = self.cp.search(vector, k, k_clusters, return_distance)
            print('cp.search_time', time.time()-bt)
            idx = results[0][0].split('@@@')[0]  # 最相似问题的索引
            return self.a_simqs(idx)  # 返回答案&相似问题的df表格

    def recall_service_api(self, sentence, k=1, k_clusters=1, return_distance=False):
        """
        函数说明：召回的API接口
        :return:
        """
        vector = sen_vec.get_sentence_vector(sentence)
        results = self.cp.search(vector, k, k_clusters, return_distance)
        return results


if __name__ == "__main__":
    rp = Recall_PySparNN(recall_by="sum_avg")
    begin_time = time.time()
    sentence = "携带管制刀具的量刑"
    answer, sim_questions = rp.search(sentence)
    print("耗时：", time.time()-begin_time)
    print('结果：', answer)
    print('其他类似案例：')
    for s_q in sim_questions:
        print(s_q)

# rp = Recall_PySparNN(recall_by="sum_avg")
# rp.insert('虐待动物')


 