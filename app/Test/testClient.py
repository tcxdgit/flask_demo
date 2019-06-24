# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
#-*- coding: utf-8 -*-
# import jieba
# def main(text):
#     return ' '.join(jieba.cut(text))
import os
import sys
sys.path.append('../')
import unicodedata
import jieba
import time
from oauth2client.client import GoogleCredentials
from six.moves import input  # pylint: disable=redefined-builtin
from concurrent.futures import ThreadPoolExecutor

from tensor2tensor import problems as problems_lib  # pylint: disable=unused-import
from tensor2tensor.serving import serving_utils
from tensor2tensor.utils import registry
from tensor2tensor.utils import usr_dir
import tensorflow as tf

from Config.Setting import SERVER
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


def Translation(input):
  start = time.time()
  tf.logging.set_verbosity(tf.logging.INFO)
  validate_flags()
  usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)
  problem = registry.problem(FLAGS.problem)
  hparams = tf.contrib.training.HParams(
      data_dir=os.path.expanduser(FLAGS.data_dir))
  problem.get_hparams(hparams)
  request_fn = make_request_fn()

  # if FLAGS.word_cut:
  #   input = " ".join(jieba.cut(input))
  outputs = serving_utils.predict(input, problem, request_fn)
  print('outputs:',outputs)
  # outputs = '.'.join(result for result,score in outputs)
  for result, _ in outputs:
      yield result

  # outputs, = outputs
  # output, score = outputs
  # end = time.time()
  # print('client time:',(end - start))
  print_str = """
Input:
{inputs}

Output (Score {score:.3f}):
{output}
    """
  # return (print_str.format(inputs=input, output=output, score=score))
  # return outputs



if __name__ == "__main__":
    ZH = '为方便用户快捷操作设备，设备支持23个快捷键。为方便用户快捷操作设备，设备支持23个快捷键。为方便用户快捷操作设备，设备支持23个快捷键。'
    zh = unicodedata.normalize("NFKC", ZH).lower()
    msg = zh.strip().split('。')
    start = time.time()
    inputs = []
    for input in msg:
        if not input == '':
            zh_jieba = ' '.join(jieba.cut(input))
            inputs.append(zh_jieba)
    res = Translation(inputs)
    # res = []
    # for input in msg:
    #     if not input == '':
    #         output = Translation(input)
    #         res.append(output)
    # 多线程
    # with ThreadPoolExecutor(2) as executor:
    #     res = executor.map(Translation, [input for input in msg if not input == ''])
    end = time.time()
    print('result:',res)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' total client time: %.2f' % (end - start))


#   flags.mark_flags_as_required(["problem", "data_dir"])
#   tf.app.run()

