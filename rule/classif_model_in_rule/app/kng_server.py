#!/usr/bin/env python
# _*_coding:utf-8 _*_

import os
import sys
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(os.path.split(root_path)[0]+"/classification")

from flask import Flask, request, abort
import json
from utils.kng_rec import EsCorpus

ec = EsCorpus()

app = Flask(__name__)


def kng_rec_api(sentence):
    search_sen = ec.search_corpus(sentence)
    return search_sen

@app.route('/kng_search_model', methods=['POST'])
def kng_search():
    """
    输入json格式{"content":"工单内容"}
    """
    if "POST" == request.method:
        req = request.data
    else:
        abort("405")
    try:
        params = str(req.decode())
        json_obj = json.loads(params)
        content = json_obj["content"]
        es_sen_dict = kng_rec_api(content)
    except Exception as err:
        print('err is:', err)
        abort(500)
    response = {}
    response['es_dict'] = es_sen_dict
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="6009", debug=True)


