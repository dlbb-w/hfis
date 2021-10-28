###############################################
# author：王奕朦
# date：2021.10.28
# 三个功能：
# 1. api().run_api(0)：根据crime.txt里的关键词，抓取相关问题和答案，生成字典database.json储存
# 2. api().insert_data(new_question, 0)：向crime.txt和database.json插入新问题new_question
# 3. api().dict2train(0)：把database.json中的问题和答案转成train.txt，用作embedding训练
###############################################
import requests
import json
import os
import re
import config

class api:
    def __init__(self):
        self.bearer = self.get_token()
        self.crime_path = os.path.join(config.root_path, 'train/crime.txt')
        self.database_path = os.path.join(config.root_path, 'train/database.json')
        self.train_path = os.path.join(config.root_path, 'train/train.txt')
        with open(self.crime_path, encoding='utf-8') as c:
            self.crime_file = c.readlines()
        with open(self.database_path, encoding='utf-8') as d:
            self.database_file = json.load(d)
        
    def get_token(self):
        """
        函数说明：获取token
        return：bearer
        """
        token_url = 'http://openapi.shiduai.com:10001/oauth/token'
        token_body = {'grant_type': 'password', 'username': 'hlj_openapi', 'password': 'heilongjiang@shiduai'}
        token_headers = {'Authorization': 'Basic bXktdHJ1c3RlZC1jbGllbnQ6c2VjcmV0', 'Content-Type': 'application/x-www-form-urlencoded'}
        post_result = requests.post(token_url, token_body, headers=token_headers)
        post_result = json.loads(post_result.content)
        bearer = post_result['token_type'] + ' ' + post_result['access_token']
        return bearer

    def get_question_similarList(self, question, bearer):
        """
        函数说明：根据关键词，即一级问题question，获取其相似（二级）问题列表
        param：question：关键词，即一级问题
               bearer：由函数get_token()得到
        return：question_similarList，question的相似问题列表
        """
        question_url = 'http://openapi.shiduai.com:10001/robot/visit/ask/new'
        question_body = {'question': question}
        question_headers = {'Authorization': bearer, 'Referer': 'http://openapi.shiduai.com:10001/robot/visit/ask/new'}
        question_result = requests.post(question_url, json=question_body, headers=question_headers)
        question_result = json.loads(question_result.content)
        question_similarList = question_result['data']['similarList']
        return question_similarList

    def  get_list(self, question_similarList, bearer):
        """
        函数说明：获取某一关键词的所有相似（二级）问题的答案（合并get_content的结果）
        param：question_similarList：某关键词的相似（二级）问题列表
               bearer：由函数get_token()得到
        return：answers：相似（二级）问题列表对应的答案列表
        """
        if question_similarList is None:
            print('没有数据')
            return
        answers=[]
        for case in question_similarList:
            answers.append(self.get_content(case, bearer))
        return answers

    def get_content(self, case, bearer):
        """
        函数说明：获取每个相似（二级）问题的答案
        param：case：某关键词的某一个相似（二级）问题
               bearer：由函数get_token()得到
        return：answer：该相似（二级）问题对应的答案
        """
        content_url = 'http://openapi.shiduai.com:10001/robot/visit/ask/new'
        content_body = {'question': case}
        content_headers = {'Authorization':bearer,'Referer':'http://openapi.shiduai.com:10001/robot/visit/ask/new'}
        content_result = requests.post(content_url, json=content_body, headers=content_headers)
        content_result = json.loads(content_result.content)
        answer = content_result['data']['answer']
        return answer

    ############################### 抓取数据主函数 ###############################
    def api_main(self, question_list, q1_count = 1, q1_dict = {} ):
        """
        函数说明：抓取数据的主函数
        param：question_list：关键词（一级）问题列表
               q1_count：用于记录（一级）问题的序号
               q1_dict：用于记录所有关键词对应的数据，格式{ q1_id: {question: q2_dict }} 
        return：q2_dict：某关键词对应的数据，格式{ q2_id: {question_similar: q2_answer}}
        """
        for question in question_list:
            question_similar_List = self.get_question_similarList(question, self.bearer)
            if question_similar_List is not None:
                # 抓取相似（二级）问题的答案
                answer_list = self.get_list(question_similar_List, self.bearer)
                q1_id = str(q1_count).zfill(3) # （一级）问题的序号，三位数表示
                q2_dict = {} # 用于记录相似（二级）问题数据
                for i, question_similar in enumerate(question_similar_List):
                    q2_id = q1_id + str(i+1).zfill(3)
                    q2_answer = re.sub(r"\<.*\>", "", answer_list[i]) # 清洗抓取到的答案
                    q2_answer = re.sub(r"\&.*\;", "'", q2_answer)
                    q2_dict.update( {q2_id: {question_similar: q2_answer}} )
                print('index is:',q1_id)
                q1_dict.update( { q1_id: {question: q2_dict }} )
                q1_count+=1
        # 抓取的问题字典，转成json文件保存
        js = json.dumps(q1_dict, indent=4, ensure_ascii=False)  # indent参数是换行和缩进
        fileObject = open(self.database_path, 'w')
        fileObject.write(js)
        fileObject.close()  # 最终写入的json文件格式:
        return q2_dict  # 返回最新插入的问题字典
    ################################################################################


############## 以下为三个功能的主函数 #######################################
    # 功能一：
    def run_api(self, start=1):
        """
        函数说明：获取（一级）问题列表，后抓取。
        param：start=0时启动执行
        return：生成database.json文件
        """
        if start == 0:
            question_list=[]
            for line in self.crime_file:
                question_list.append(line.replace('\n',''))
            self.api_main(question_list)
        return

    # 功能二：
    def insert_data(self, question, start=1):
        """
        函数说明：向问题列表crime，和已抓取的文件database，插入新问题question。
        param：question：要抓取的新问题
        param：start：=0时启动执行
        return：生成database.json文件
        """
        if (self.get_question_similarList(question, self.bearer) is not None) & (start==0):
            q1_counts = int(list(self.database_file.keys())[-1])+1
            insert_dict = self.api_main([question], q1_counts, self.database_file)  # 向已抓取的文件database插入新问题
            with open(self.crime_path, 'a', encoding='utf-8') as new_c:
                new_c.write('\n'+question)  # 向问题列表crime插入新问题
            return insert_dict

    # 功能三：
    def dict2train(self, start=1):
        """
        函数说明：根据抓取的问题字典，取相似（二级）问题和其答案生成train.txt文件
        param：start：=0时启动执行
        return：生成train.txt文件。
        """
        with open(self.train_path, 'w') as f:
            for q1_q2as in list(self.database_file.values()):
                train_txt = list(list(q1_q2as.values())[0].values()) # 每个一级问题下二级问题和答案的列表
                for i in range(len(list(train_txt))):
                    for key, values in train_txt[i].items():
                        f.write(key+","+values+"\r")
            f.close()


apii = api()
# 1换成0，启动api，生成database.json
apii.run_api(1) 
# 1换成0，启动插入新数据，更新database.json
apii.insert_data('虐待动物', 1)
# 1换成0，更新train.txt做embedding训练，一般不用
apii.dict2train(1)

# # url = 'http://openapi.shiduai.com:10001/oauth/token'
# # html = requests.get(url).text 
# # response = json.loads(html)
# # print(html)

