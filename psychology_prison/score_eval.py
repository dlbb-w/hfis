###############################################
# 统计数值型量表的得分（量表总分，各个系列的总分），并评估区间。
# Author: wangyimeng
# Date: 2021/10/28 
# 输入：原始量表{'1':'3', '2':'1', ...}
# 输出：危险指数 或 等级评价
# 实现的量表有：'CX', 'XT', 'jiaolv', 'yiyu', 'SCL90', 'RW'
###############################################

import json
from collections import Counter

# CX量表
def cx(dict_score):
    score = sum(dict_score.values())
    if 0 <= score <= 5:
        prob = 0.000; level = '低'
    if 6 <= score <= 10:
        prob = 0.073; level = '低'
    if 11 <= score <= 15:
        prob = 0.152; level = '低'
    if 16 <= score <= 20:
        prob = 0.281; level = '低'
    if 21 <= score <= 25:
        prob = 0.428; level = '中'
    if 26 <= score <= 30:
        prob = 0.541; level = '中'
    if 31 <= score <= 35:
        prob = 0.652; level = '中'
    if 36 <= score <= 40:
        prob = 0.787; level = '高'
    if 41 <= score <= 45:
        prob = 0.923; level = '高'
    if 46 <= score <= 50:
        prob = 1.000; level = '高'
    return prob, level

# XT量表
def xt(dict_score):
    score = sum(dict_score.values())
    if 0 <= score <= 35:
        assess = '刑罚体验很浅'; level = '高'
    if 36 <= score <= 70:
        assess = '刑罚体验一般'; level = '中'
    if 71 <= score <= 100:
        assess = '刑罚体验很深'; level = '低'
    return assess, level

# 抑郁量表
def yiyu(dict_score):
    score = int(sum(dict_score.values())*1.25) # 标准分
    if score <= 52:
        assess = '无抑郁'
    elif 53 <= score <= 62:
        assess = '轻度抑郁'
    elif 63 <= score <= 72:
        assess = '中度抑郁'
    else:
        assess = '重度抑郁'
    return assess

# 焦虑量表
def jiaolv(dict_score):
    score = int(sum(dict_score.values())*1.25) # 标准分
    if score < 50:
        assess = '无焦虑'
    elif 50 <= score <= 59:
        assess = '轻度焦虑'
    elif 60 <= score <= 69:
        assess = '中度焦虑'
    else:
        assess = '重度焦虑'
    return assess

global SCL90_idx_dict
SCL90_idx_dict = {'1.躯体化': [1, 4, 12, 27, 40, 42, 48, 49, 52, 53, 56, 58], # (1)躯体化
            '2.强迫症状': [3, 9, 10, 28, 38, 45, 46, 51, 55, 65], # (2)强迫症状
            '3.人际关系敏感': [6, 21, 34, 36, 37, 41, 61, 69, 73], # (3)人际关系敏感
            '4.抑郁': [5, 14, 15, 20, 22, 26, 29, 30, 31, 32, 54, 71, 79], # (4)抑郁
            '5.焦虑': [2, 17, 23, 33, 39, 57, 72, 78, 80, 86], # (5)焦虑
            '6.敌对': [11, 24, 63, 67, 74, 81], # (6)敌对
            '7.恐怖': [13, 25, 47, 50, 70, 75, 82], # (7)恐怖
            '8.偏执': [8, 18, 43, 68, 76, 83], # (8)偏执
            '9.精神病性': [7, 16, 35, 62, 77, 84, 85, 87, 88, 90], # (9)精神病性
            '10.其他': [19, 44, 59, 60, 64, 66, 89]} # (10)其他：睡眠及饮食
# 90项症状
def SCL90(dict_score):
    score_l = dict( zip( list(SCL90_idx_dict.keys()), [0 for i in range(10)] )) # 记录各因子分数
    for i,idx_l in SCL90_idx_dict.items():
        for idx in idx_l:
            score_l[i] += dict_score[str(idx)] # 为10项因子计算得分
    score_l.update({'11.总分':sum(score_l.values())}) # 计算总分
    assess = []
    if score_l['11.总分'] > 160:
        assess.append('总分高，需进一步检查') 
    if score_l['1.躯体化'] > 36:
        assess.append('1.躯体化分高，表明个体在身体上有较明显的不适感，并常伴有头痛、肌肉酸痛等症状。')
    if score_l['2.强迫症状'] > 30:
        assess.append('2.强迫症状分高，强迫症状较明显。') 
    if score_l['3.人际关系敏感'] > 27:
        assess.append('3.人际关系敏感分高，表明个体人际关系较为敏感，人际交往中自卑感较强，并伴有行为症状（如坐立不安，退缩等）。')
    if score_l['4.抑郁'] > 39:
        assess.append('4.抑郁分高，表明个体的抑郁程度较强，生活缺乏足够的兴趣，缺乏运动活力，极端情况下，可能会有想死亡的思想和自杀的观念。') 
    if score_l['5.焦虑'] > 30:
        assess.append('5.焦虑分高，表明个体较易焦虑，易表现出烦躁、不安静和神经过敏，极端时可能导致惊恐发作。')
    if score_l['6.敌对'] > 18:
        assess.append('6.敌对分高，表明个体易表现出敌对的思想、情感和行为。') 
    if score_l['7.恐怖'] > 21:
        assess.append('7.恐怖分高，表明个体恐怖症状较为明显，常表现出社交、广场和人群恐惧。') 
    if score_l['8.偏执'] > 18:
        assess.append('8.偏执分高，表明个体的偏执症状明显，较易猜疑和敌对。')
    if score_l['9.精神病性'] > 30:
        assess.append('9.精神病性分高，表明个体的精神病性症状较为明显。') 
    if score_l['10.其他'] > 21:
        assess.append('10.其他项目（睡眠、饮食等）分高。') 

    pos_num = 90-Counter(dict_score.values())[1] # 阳性项目数
    if pos_num > 43:
        assess.append('阳性项目多，需进一步检查') 
        pos_idx = [k for k,v in dict_score.items() if v>1 ] # 阳性项目的序号
        assess += pos_idx
    return assess

# RW量表
def rw(dict_score, model):
    """
    输入参数：
        dict_score：字典形式储存的问卷得分
        model：用哪个测试模型，可选择域['<10', '>10', '女']
    输出参数：
        每个类别的得分score, 对应的常模分布的均值avg, 所处区间评价assess, 改造难度change, 关押等级jail
    """
    # 计算量表总分
    D_score=0; E_score=0; F_score=0; X_score=0; Y_score=0; Z_score=0
    for idx, score in dict_score.items():
        if idx[0] == 'D':       # 涉毒
            D_score += score
        elif idx[0] == 'E':     # 恶习状况
            E_score += score
        elif idx[0] == 'F':     # 犯罪状态
            F_score += score
        elif idx[0] == 'X':     # 心理生理状态
            X_score += score
        elif idx[0] == 'Y':     # 犯罪归因
            Y_score += score
        elif idx[0] == 'Z':     # 自然状况
            Z_score += score
    A_score = D_score+E_score+F_score+X_score+Y_score+Z_score  # 总分
    sum_score = {'D':D_score, 'E':E_score, 'F':F_score, 'X':X_score, 'Y':Y_score, 'Z':Z_score, 'A':A_score}
    
    res_dict = {}
    # 根据总分评估量表
    for type,score in sum_score.items():
        if model == '<10':  # 不满10年RW量表分数
            if type == 'D':       # 涉毒
                avg = 0.15; standard = [2,5]
            elif type == 'E':     # 恶习状况
                avg = 7.66; standard = [6,9]
            elif type == 'F':     # 犯罪状态
                avg = 18.3; standard = [15,22]
            elif type == 'X':     # 心理生理状态
                avg = 2.73; standard = [2,4]
            elif type == 'Y':     # 犯罪归因
                avg = 1.75; standard = [2,5]
            elif type == 'Z':     # 自然状况
                avg = 11.89; standard = [9,14]
            elif type == 'A':     # 总分
                avg = 42.46; standard = [34,51]

        elif model == '>10':  # 10年以上RW量表分数
            if type == 'D':       # 涉毒
                avg = 0.3; standard = [2,5]
            elif type == 'E':     # 恶习状况
                avg = 8.42; standard = [7,10]
            elif type == 'F':     # 犯罪状态
                avg = 24.81; standard = [20,30]
            elif type == 'X':     # 心理生理状态
                avg = 4.71; standard = [4,6]
            elif type == 'Y':     # 犯罪归因
                avg = 2.54; standard = [2,5]
            elif type == 'Z':     # 自然状况
                avg = 11.76; standard = [9,14]
            elif type == 'A':     # 总分
                avg = 52.54; standard = [42,63]

        elif model == '女':  # 女性RW量表分数
            if type == 'D':       # 涉毒
                avg = 0.6; standard = [2,5]
            elif type == 'E':     # 恶习状况
                avg = 4.67; standard = [3,6]
            elif type == 'F':     # 犯罪状态
                avg = 16.37; standard = [13,20]
            elif type == 'X':     # 心理生理状态
                avg = 3.4; standard = [2,4]
            elif type == 'Y':     # 犯罪归因
                avg = 1.03; standard = [2,5]
            elif type == 'Z':     # 自然状况
                avg = 10.13; standard = [8,12]
            elif type == 'A':     # 总分
                avg = 36.17; standard = [29,43]

        if score < standard[0]:
            assess = '稳定区'; change = '易'; jail = '低'
        if standard[0] <= score < standard[1]:
            assess = '相对稳定区'; change = '较难'; jail = '中'
        if score >= standard[1]:
            assess = '危险区'; change = '难'; jail = '高'
        res_dict.update({type:{'得分':score, '常模平均值':avg, '区间评价':assess, '改造难度':change, '关押等级':jail}})
    return res_dict

# if __name__ == '__main__':
#     with open('database_score/CX.json','r',encoding='utf8')as f:
#         json_data = json.load(f)
#     cx(json_data)

