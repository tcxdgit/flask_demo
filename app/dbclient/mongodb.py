#-*- coding: utf-8 -*-
'''
@Author  :wu jiefang
@Time    : 2019/5/5 11:11
@Software: PyCharm
@Email   :wu.jiefang@h3c.com    
@File    : mongodb.py
'''
import datetime
import pymongo
import sys
sys.path.append("..")
# from app.Config.Setting import Dbdata
from Config.Setting import Dbdata
# Dbdata = {"host": "127.0.0.1",
#           "port": 27017,
#           "db_name": "Tranlation",
#           "col": "trans"
# }
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(filename)s[%(lineno)d] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
class Mongodb_Operator():
    def __init__(self):
        host = Dbdata['host']
        port = Dbdata['port']
        db_name = Dbdata['db_name']
        col = Dbdata['col']
        # self.client = pymongo.MongoClient(host=host,
        #                                   port=port,connect=False)  # Connection() 和 MongoClient() safe MongoClient被设计成线程安全、可以被多线程共享的
        self.client = pymongo.MongoClient(host=host,port=port)
        self.db = self.client[db_name]
        self.col = self.db[col]
    def insert_db(self,input,output):
        logger.info('zh:{}'.format(input))
        logger.info('en:{}'.format(output))
        for i in range(len(input)):
            currenttime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            data = {
                "zh-Hans":input[i],
                "en-US":[output[i]],
                "time":currenttime

            }
            res = self.col.find_one({"zh-Hans":input[i]})
            # print('res:',res)
            if not res:
                # print(self.col)
                self.col.insert_one(data)

            else:
                en = res['en-US']
                if output[i] in en:
                    logger.warning('has exists in DB')
                else:
                    data['en-US'] = res['en-US'] + [output[i]]
                    self.col.update({'zh-Hans': input[i]},{'$set': {'en-US': data['en-US'], 'time': data['time']}})
                    logger.info('update DB successfully')

    def test(self):
        res = self.col.find()
        for i in res:
            print(i)

if __name__ == '__main__':
    mongo = Mongodb_Operator()
    # mongo.insert_db('aa','bb')
    mongo.test()


