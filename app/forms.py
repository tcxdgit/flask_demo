# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     hello
   Author :       'louzhu'
   date:          2019/4/27 22:47
-------------------------------------------------
   Change Activity:
                    2019/4/27:
-------------------------------------------------
"""
__author__ = 'louzhu'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

class Form(FlaskForm):
    input = TextAreaField('输入待翻译的中文句子', validators=[DataRequired()])
    trans = SubmitField('翻译')
    output = TextAreaField('翻译结果')
    saver = SubmitField('保存')


