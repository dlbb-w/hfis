#!/usr/bin/env python
# _*_coding:utf-8 _*_

import os
import sys
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(os.path.split(root_path)[0]+"/classification")

from flask import Flask, request, abort
import json
from utils.ltp_analyse import LtpParser

ltp = LtpParser()
app = Flask(__name__)

def relation_ext_api(org_sentence):
    rel_sen = ltp.analyse(org_sentence)
    return rel_sen


@app.route('/relation_ext_model', methods=['POST'])
def rel_model():
    """
    输入json格式{"content":"亲属关系原句"}
    """
    if "POST" == request.method:
        req = request.data
    else:
        abort("405")
    try:
        params = str(req.decode())
        json_obj = json.loads(params)
        content = json_obj["content"]
        relatives_list = relation_ext_api(content)
    except Exception as err:
        print('err is:', err)
        abort(500)
    response = {}
    response['rel_list'] = relatives_list
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="6007", debug=True)


