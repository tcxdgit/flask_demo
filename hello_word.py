# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     hello__word
   Author :       'louzhu'
   date:          2019/4/21 17:42
-------------------------------------------------
   Change Activity:
                    2019/4/21:
-------------------------------------------------
"""
__author__ = 'louzhu'
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')
    # return '<h1>hello world!</h1>'
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)
if __name__ == '__main__':
    app.run(debug=True)
