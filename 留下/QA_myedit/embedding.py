"""
训练word2vec模型
Author: Shubao Zhao
"""
import os
import sys
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
root_path = os.path.split(root_path)[0]
print("root_path = ", root_path)
sys.path.append(root_path)

from src.utils import cut_sentence
import pandas as pd
from gensim import models
from gensim.models import word2vec
import config
import logging
from tqdm import tqdm


logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


""
class Embedding:
    """
    实现一个Embedding类，训练词向量
    """
    def __init__(self, by_word=False):
        print("创建Embedding类....................")
        self.root_path = config.root_path
        print(self.root_path)
        self.original_path = os.path.join(self.root_path, "datasets/train")  # 数据集路径
        if by_word:
            self.train_file_path = os.path.join(self.root_path, "train/train_by_word.txt")
        else:
            self.train_file_path = os.path.join(self.root_path, "train/train.txt")
        self.by_word = by_word
        print("加载数据......................")


    def get_data(self, file_path):
        """
        函数说明：利用pandas读取excel文件
        :param file_path: 读取的文件路径
        :return: data
        """
        data = pd.read_excel(file_path, header=0, names=["label", "content"])
        return data

    def preprocess(self):
        """
        函数说明：读取原始数据文件,并进行分词处理
        :return:
        """
        f = open(self.train_file_path, "w+", encoding="utf-8") # 打开要写入的文件的路径
        # for root, dirs, files in os.walk(self.original_path):
        #     # 遍历每一个数据集
        #     for file in tqdm(files):
        #         file_path = os.path.join(root, file)
        #         if "DS_Store" in file_path:
        #             continue
        #         print("file_path = ", file_path)
        #         data = self.get_data(file_path)
        #         for index, row in data.iterrows():
        #             print("row[content] = ", row["content"])
        #             sentence = row["content"]
        #             # 处理空数据
        #             if type(sentence) == float:
        #                 # 如果内容为空，则跳过
        #                 continue
        #             if len(sentence) <= 3:
        #                 # 字数太少则跳过
        #                 continue
        with open(self.train_file_path,'r') as rf:
            for sentence in rf:
                sentence = cut_sentence.cut(sentence, by_word=False, use_stopword=True)
                print(sentence)
                for word in sentence:
                    f.write(word + "\t")
                f.write("\n")
                f.close()
        logger.info("数据预处理完成，包括分词和写入到本地文件")

    def train_word2vec(self):
        """
        函数说明：通过word2vec训练词向量
        :return:
        """
        print("训练词向量...................")
        sentence = word2vec.PathLineSentences(self.train_file_path)
        self.w2v = models.Word2Vec(min_count=1,
                                   window=5,
                                   vector_size=300,
                                   sample=6e-5,
                                   alpha=0.03,
                                   min_alpha=0.0007,
                                   negative=100,
                                   workers=4,
                                   epochs=50,
                                   sg=1,
                                   max_vocab_size=50000)
        self.w2v.build_vocab(sentence)
        self.w2v.train(sentence,
                       total_examples=self.w2v.corpus_count,
                       epochs=50,
                       report_delay=1)
        print("词向量训练完成............................")

    def save_word2vec(self):
        """
        函数说明：保存word2vec训练的词向量
        :return:
        """
        print("保存词向量模型..............................")
        if self.by_word:
            self.w2v.wv.save_word2vec_format(self.root_path + "/model/embedding/w2v_300_by_word.bin", binary=False)
        else:
            self.w2v.wv.save_word2vec_format(self.root_path + "/model/embedding/w2v_300_MAS.bin", binary=False)


    def load_word2vec(self):
        """
        函数说明：加载word2vec训练的词向量
        :return:
        """
        if self.by_word:
            self.w2v = models.KeyedVectors.load_word2vec_format(
                self.root_path + "/model/embedding/w2v_300_by_word.bin", binary=False)
            return self.w2v
        else:
            self.w2v = models.KeyedVectors.load_word2vec_format(
                self.root_path + "/model/embedding/w2v_300.bin", binary=False)
            return self.w2v



if __name__ == "__main__":
    em = Embedding(by_word=False)
    em.preprocess()
    em.train_word2vec()
    em.save_word2vec()