# -*- coding: utf-8 -*-

from flask import Flask, helpers, request
from flask_cors import CORS
from twiimg import TwiimgHandler
from sfen import SfenHandler
from resize import ResizeHandler

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
CORS(app)
# default response header

headers = {
    'Access-Control-Allow-Origin': '*'
}

@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response
    
# /twiimg にアクセスしたときの処理
@app.route('/twiimg', methods=['GET'])
def get1():
    twiimgHandler = TwiimgHandler(request.url_root, request.args, request.query_string)
    result = twiimgHandler.get()
    if result[0] == 200:
        return app.response_class(result[1], headers=headers)
    else:
        return app.response_class(result[1], status=result[0], headers=headers)

# /twiimg にアクセスしたときの処理
@app.route('/sfen', methods=['GET'])
def get2():
    sfenHandler = SfenHandler(request.url, request.args, request.query_string)
    result = sfenHandler.get()
    if result[0] == 200:
        return app.response_class(result[1], content_type='image/png', headers=headers)
    else:
        return app.response_class(result[1], status=result[0], headers=headers)
    
# /twiimg にアクセスしたときの処理
@app.route('/resize', methods=['GET'])
def get3():
    resizeHandler = ResizeHandler(request.url_root, request.args, request.query_string)
    result = resizeHandler.get()
    if result[0] == 200:
        return app.response_class(result[1], content_type='image/png', headers=headers)
    else:
        return app.response_class(result[1], status=result[0], headers=headers)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, threaded=True)