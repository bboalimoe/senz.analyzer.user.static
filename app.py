# coding: utf-8

from datetime import datetime

from flask import Flask,request
from flask import render_template
from static_info import InfoGetter
from views.todos import todos_view
import json
app = Flask(__name__)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())


@app.route("/static_info", methods=['GET'])
def get_static_info():
    if request.method == 'GET':
        apps = request.args.get('app_list')
        print apps
        if not apps:
            return '{"error":"param error:no app_list"}'

        i = InfoGetter()
        return json.dumps(i.get_labels(apps.split(',')))

    return "Please use GET!"




if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)