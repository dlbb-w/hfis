# -*- coding: utf-8 -*-
# Author:chenyipin
# Date:2021/9/15
##########################
# 热线内容 容错匹配 修改的is_matched函数，在match.py文件里
# Author:wangyimeng
# Date:2021/10/28
##########################

from classify_rule import load_rule_classify_model

class classifyModel():
    def __init__(self):
        self.type_model = load_rule_classify_model()

    def predict(self,sentence):
        '''
        :param sentence:工单内容
        :return: 类型
        '''

        model_score = self.get_model_score(sentence)
        predict_type = 'ELSE'
        thresd = 9
        # 每个类型的得分
        for type,score in model_score.items():
            print(type,score)
            if score > thresd:
                predict_type = type
                thresd = score
        return predict_type


    def get_model_score(self,sentence):
        '''
        每个模型的得分
        :param sentence:
        :return:模型得分，存在一个dict里面
        '''
        model_score = {}
        rules = self.type_model
        for type, models in rules.items():
            score = 0
            for sub_model in models:
                flag = 1
                ssub_score = 0
                for rule in sub_model:
                    wordType = rule.wordType
                    wordScore = rule.wordScore
                    sub_score, sub_flag = self.get_score_change(wordType, wordScore, sentence)##每条规则的得分
                    # print(wordType,'-----',wordScore,'-----',sub_score,'------',sub_flag)
                    flag = flag * sub_flag
                    ssub_score += sub_score##每个occursametime的得分
                score += ssub_score * flag ##每个模型的总得分
            model_score[type] = score
        return model_score



    def get_score_change(self,wordType,wordScore,sentence):
        '''
        :param wordType:
        :param wordScore:
        :param sentence:
        :return:
        '''
        score = 0
        sub_Flag = 0
        for key_words,confirm in wordType.items():
            key_word = key_words.split(',')
            it_score = wordScore[key_words]
            if confirm == 'contain':
                for kw in key_word:
                    if kw in sentence:
                        return it_score, 1
                return it_score, 0
            if confirm == 'uncontain':
                for kw in key_word:
                    if kw in sentence:
                        return it_score, 0
                return it_score, 1
            # match_party = billImage.part_dict[confirm.split('@@')[0]].replace(' ','')
            # if confirm == 'contain':
            #     for kw in key_word:
            #         kw = kw.replace(' ','')
            #         if self.is_matched(kw,match_party):
            #             score  =  it_score
            #             sub_Flag  = 1
            #         else:
            #             sub_Flag = sub_Flag + 0
            # if confirm == 'uncontain':
            #     for kw in key_word:
            #         kw = kw.replace(' ','')
            #         if self.is_matched(kw,match_party):
            #             sub_Flag = sub_Flag * 0
            #         else:
            #             score = it_score
            #             sub_Flag = 1
        # return score,sub_Flag


    def is_matched(self,key_word,match_party):
        '''
        设置一定的容错率：小于4的关键字不允许出错，大于4的允许一个，大于6允许错两个。。。。。。
        :param key_word:关键字
        :param match_party:匹配字段
        :return:
        '''
        flag = False
        key_len = len(key_word)
        str_len = len(match_party)
        if str_len < key_len:
            flag = False
        else:
            if key_len < 4:
                if key_word in match_party:
                    return True
                else:
                    return False
            else:
                for index in range(0,str_len - key_len+1):
                    sub_string = match_party[index:index+key_len]
                    matched_char_num = 0
                    for i, char in enumerate(sub_string):
                        if char == key_word[i]:
                            matched_char_num += 1
                    matched_rate = matched_char_num / key_len
                    if matched_rate > 0.83333:
                        return True
        return flag


if __name__ == '__main__':
    cm = classifyModel()
    sentence = '来电人投诉：恒大绿洲对面工地每天早上5点多开始施工，噪音扰民。'
    print(cm.predict(sentence))
