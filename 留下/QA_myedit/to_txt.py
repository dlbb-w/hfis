
import json
with open('database.json') as f:
        data = json.load(f)
data = list(data.values())
with open('train.txt', 'w') as f:
    for q1_q2as in data:
        to_txt = list(list(q1_q2as.values())[0].values()) # 每个一级问题下二级问题和答案的列表
        for i in range(len(list(to_txt))):
            for key, values in to_txt[i].items():
                f.write(key+","+values+"\r")
    f.close()