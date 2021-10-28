#!/usr/bin/env python
# _*_coding:utf-8 _*_

import os
import sys
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(os.path.split(root_path)[0]+"/classification")

from flask import Flask, request, abort
import json
from ml_classify.classify_model_predict import CModel

m = CModel('svm')

app = Flask(__name__)


def classify_api(input_text):
    label = m.predict(input_text)
    return label


@app.route('/classify_model',methods=['POST'])
def cls_model():
    """
    输入json格式{"content":"内容"}
    输出json格式{"label":0}
    """
    if "POST" == request.method:
        req = request.data
    else:
        abort("405")
    try:
        params = str(req.decode())
        json_obj = json.loads(params)
        content = json_obj["content"]
        label = classify_api(content)
    except Exception as err:
        print('err is:',err)
        abort(500)
    response = {}
    response['label_cls'] = label
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="6002", debug=True)


