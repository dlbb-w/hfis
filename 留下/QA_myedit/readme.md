author：王奕朦
date：2021.10.28

文件说明：
法律知识问答机器人，输入要查询的问题，返回问题答案和相似问题列表（/src/recall/recall_pysparnn.py）。
可以用recall_pysparnn.py中的插入函数完善数据库，也可以更新crime.txt文件重新抓取数据和训练模型。

文件执行顺序：
1. shiduAPI.py：根据crime.txt中的问题，抓取数据，生成训练模型所要的数据文件（train.txt和database.json）
2. /src/word2vec/embedding.py：用train.txt训练embedding模型，储存在/model/embedding/
3. /src/recall/recall_pysparnn.py：用database.json训练recall模型，储存在/model/recall/。可用search函数做问题的相似查找，返回答案和相似问题。