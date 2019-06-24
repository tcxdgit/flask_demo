#-*- coding: utf-8 -*-
'''
@Author  :wu jiefang
@Time    : 2019/4/28 15:21
@Software: PyCharm
@Email   :wu.jiefang@h3c.com    
@File    : client.py
'''
import os
import re
import time
import unicodedata

from flask import request
from flask_bootstrap import Bootstrap
from flask import Flask,render_template,session, redirect, url_for,abort,flash
from forms import Form
from dbclient.mongodb import Mongodb_Operator
import os
from oauth2client.client import GoogleCredentials
from six.moves import input  # pylint: disable=redefined-builtin

from tensor2tensor import problems as problems_lib  # pylint: disable=unused-import
from tensor2tensor.serving import serving_utils
from tensor2tensor.utils import registry
from tensor2tensor.utils import usr_dir
import tensorflow as tf
import jieba
# #load jieba model
jieba.load_userdict('userdict.txt')
jieba.cut('')
# from jieba import Tokenizer
from Config.Setting import SERVER
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(filename)s[%(lineno)d] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


flags = tf.flags
FLAGS = flags.FLAGS

flags.DEFINE_string("server", SERVER['host'], "Address to Tensorflow Serving server.")
flags.DEFINE_string("servable_name", SERVER['servable_name'], "Name of served model.")
flags.DEFINE_string("problem", SERVER['problem'], "Problem name.")
flags.DEFINE_string("data_dir", SERVER['data_dir'], "Data directory, for vocab files.")
flags.DEFINE_string("t2t_usr_dir", SERVER['t2t_usr_dir'], "Usr dir for registrations.")
flags.DEFINE_string("inputs_once", None, "Query once with this input.")
flags.DEFINE_integer("timeout_secs", SERVER['timeout_secs'], "Timeout for query.")
flags.DEFINE_boolean("word_cut", SERVER['word_cut'], "Weather use word cut.")

# For Cloud ML Engine predictions.
flags.DEFINE_string("cloud_mlengine_model_name", None,
                    "Name of model deployed on Cloud ML Engine.")
flags.DEFINE_string(
    "cloud_mlengine_model_version", None,
    "Version of the model to use. If None, requests will be "
    "sent to the default version.")


def validate_flags():
  """Validates flags are set to acceptable values."""
  if FLAGS.cloud_mlengine_model_name:
    assert not FLAGS.server
    assert not FLAGS.servable_name
  else:
    assert FLAGS.server
    assert FLAGS.servable_name


def make_request_fn():
  """Returns a request function."""
  if FLAGS.cloud_mlengine_model_name:
    request_fn = serving_utils.make_cloud_mlengine_request_fn(
        credentials=GoogleCredentials.get_application_default(),
        model_name=FLAGS.cloud_mlengine_model_name,
        version=FLAGS.cloud_mlengine_model_version)
  else:

    request_fn = serving_utils.make_grpc_request_fn(
        servable_name=FLAGS.servable_name,
        server=FLAGS.server,
        timeout_secs=FLAGS.timeout_secs)
  return request_fn

tf.logging.set_verbosity(tf.logging.INFO)
validate_flags()
usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)
problem = registry.problem(FLAGS.problem)
hparams = tf.contrib.training.HParams(
  data_dir=os.path.expanduser(FLAGS.data_dir))
problem.get_hparams(hparams)
request_fn = make_request_fn()
def translation(inputs):
    logger.info('translate sents:{}'.format(inputs))

    start1 = time.time()
    outputs = serving_utils.predict(inputs, problem, request_fn)
    outputs = ''.join(result for result,score in outputs)
    outputs = outputs.replace('< / EOP >', '\r\n')
    end1 = time.time()
    logger.info('cline:%.2f' % (end1-start1))

  # return (print_str.format(inputs=input, output=output, score=score))
    return outputs

app = Flask(__name__)
# print(app)
app.config['SECRET_KEY'] = '123456'
bootstrap = Bootstrap(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        zh = unicodedata.normalize('NFKC', form.input.data)
        if form.trans.data:
            # print('input:',form.input.data)
            logger.info('zh:%s' % zh)
            msg = re.sub('([。!?])([^”’])',r"\1\n\2",zh)
            msg = re.sub('(\.{6})([^”’])',r"\1\n\2",msg)
            msg = re.sub('([。!?][”’])([^,。!?])',r"\1\n\2",msg)
            msg = re.sub('(.*)(\r\n)', r"\1\n\2", msg)
            msg = msg.strip().split('\n')
            # msg = zh.strip()
            logger.info('msg:%s' % msg)
            start = time.time()
            inputs = []
            for i in range(len(msg)):
                if msg[i] == '\r':
                    msg[i] = '</EOP>'
                if not msg[i] == '':
                    # zh_list = list(jieba.cut(msg[i]))
                    # #delete ' '
                    # while ' ' in zh_list:
                    #     zh_list.remove(' ')
                    zh_jieba = ' '.join(jieba.cut(msg[i]))
                    zh_jieba = re.sub(" {2,}", " ", zh_jieba)
                    inputs.append(zh_jieba.strip())
            res = translation(inputs)
            logger.info('original res:%s' % res)
            res = unicodedata.normalize('NFKC', res)
            res = re.sub(" {2,}", " ", res)
            res = re.sub(" ,", ",", res)
            res = re.sub("’", "'", res)
            res = re.sub("“ ", "\"", res)
            res = re.sub("' ", "'", res)
            res = re.sub(" '", "'", res)
            res = re.sub(" ”", "\"", res)
            res = re.sub("‘ ", "'", res)
            res = re.sub(" _ ","_",res)
            res = re.sub(" : ",":",res)
            res = re.sub(" / ","/",res)
            res = re.sub(" — ","—",res)
            res = re.sub("\( ","(",res)
            res = re.sub(" \)",")",res)
            res = re.sub("< ","<",res)
            res = re.sub(" >",">",res)
            res = re.sub("\$ ","$",res)
            res = re.sub(" \.",". ",res)
            end = time.time()
            logger.info('total client time:%.2f'%(end-start))
            form.output.data = res
        if form.saver.data:
            if not form.output.data:
                flash('翻译结果不能为空')
            else:
                data_insert = Mongodb_Operator()
                zh_list = zh.strip().split('\r\n')
                zhlist = [zh_l for zh_l in zh_list if not zh_l == '']
                en_list = form.output.data.strip().split('\r\n')
                enlist = [en_l for en_l in en_list if not en_l == '']
                if len(zhlist) == len(enlist):

                    data_insert.insert_db(zhlist, enlist)
                else:
                    data_insert.insert_db([zh.strip()], [form.output.data])
                flash('保存成功')
                #logger.info(form.output.data)
                logger.info('save into DB successfully')

    return render_template('index.html',form=form)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)
