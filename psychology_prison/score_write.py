###############################################
# 将原始量表的选项，改写为数值格式的分值。 
# 假设原始量表形式：{'1':'A', '2':'C', ...}，改写为对应分值{'1':'3', '2':'1', ...}
# 实现的量表有：'CX', 'XT', 'jiaolv', 'yiyu'
# Author: wangyimeng
# Date: 2021/10/28 
###############################################

import json

def write(file_name):

    # 打开存储数值分数的字典，记为dict_score
    with open('database_score/'+file_name+'.json','r',encoding='utf8')as f:
        dict_score = json.load(f)
    # 打开原始文件，记为file
    with open('database_original_file/'+file_name+'.json','r',encoding='utf8')as f:
        file = json.load(f)


    if file_name == 'yiyu':
        neg = {'A':1, 'B':2, 'C':3, 'D':4} # 准则
        pos = {'A':4, 'B':3, 'C':2, 'D':1} # 反向记分准则
        for idx in ['2', '5', '6', '11', '12', '14', '16', '17', '18', '20']: # 反向记分
            dict_score[idx] = pos[file[idx]]
        for idx in ['1', '3', '4', '7', '8', '9', '10', '13', '15', '19']: 
            dict_score[idx] = neg[file[idx]]


    if file_name == 'jiaolv':
        neg = {'A':1, 'B':2, 'C':3, 'D':4} # 准则
        pos = {'A':4, 'B':3, 'C':2, 'D':1} # 反向记分准则
        for idx in list(dict_score.keys()):
            if idx in ['5', '9', '13', '17', '19']: # 反向记分
                dict_score[idx] = pos[file[idx]]
            else: 
                dict_score[idx] = neg[file[idx]]

    if file_name == 'XT':
        neg = {'符合':2, '难以确定':1, '不符合':0} # 消极项得分准则
        pos = {'符合':0, '难以确定':1, '不符合':2} # 积极项得分准则，反向积分
        for idx in list(dict_score.keys()):
            if idx in ['9', '16', '25', '30']: # 积极，反向记分
                dict_score[idx] = pos[file[idx]]
            else:
                dict_score[idx] = neg[file[idx]]
    
    if file_name == 'CX':
        rule1 = {'符合':1, '不符合':0} # 准则1：有些选项得分为1
        rule2 = {'符合':2, '不符合':0} # 准则2：有些选项得分为2
        rule3 = {'符合':3, '不符合':0} # 有些选项得分为3
        rule4 = {'符合':4, '不符合':0} # 有些选项得分为4
        for idx in list(dict_score.keys()):
            if idx in ['2', '4', '6', '10', '12', '17', '20', '23', '24']: # 准则1
                dict_score[idx] = rule1[file[idx]]
            elif idx in ['1', '5', '8', '11', '13', '15', '21', '22']: # 准则2
                dict_score[idx] = rule2[file[idx]]
            elif idx in ['3', '7', '9', '14', '16', '19', '25']: # 准则3
                dict_score[idx] = rule3[file[idx]]
            else: # 准则4
                dict_score[idx] = rule4[file[idx]]

    # 重新生成database中的score文件
    json_f = open('database_score/'+file_name+'.json', 'w')
    json_f.write( json.dumps(dict_score, indent=4, ensure_ascii=False) )
    json_f.close()
    return dict_score

# if __name__ == '__main__':
#     for file_name in ['90', 'COPA', 'CX', 'jiaolv', 'RW', 'XT', 'yiyu']:
#         write(file_name)
