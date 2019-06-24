#-*- coding: utf-8 -*-
'''
@Author  :wu jiefang
@Time    : 2019/5/5 10:50
@Software: PyCharm
@Email   :wu.jiefang@h3c.com    
@File    : Setting.py
'''
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--SERVER_IP_PORT', default='10.99.210.212:8000')
parser.add_argument('--DB_IP', default='10.99.210.212')
args = parser.parse_args()
SERVER = {
    "host":"10.99.210.212:8008",
    # "host":args.SERVER_IP_PORT,  #Address to Tensorflow Serving server
    "servable_name":"transformer",  #Name of served model
    "problem":"translate_zhen_ai",  #Problem name
    # "data_dir":"/app/t2t_data",  #Data directory, for vocab files
    "data_dir":"./t2t_data",  #Data directory, for vocab files
    # "t2t_usr_dir":"/app/self_script/",  #Usr dir for registrations
    "t2t_usr_dir":"./self_script/",  #Usr dir for registrations
    "timeout_secs":300,  #Timeout for query
    "word_cut":True   #Weather use word cut
}

Dbdata = {
          "host": "10.99.210.212",
          # "host": args.DB_IP,
          "port": 27017,
          "db_name": "ML_Translation",
          "col": "trans"
}