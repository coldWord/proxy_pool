# -*- coding: utf-8 -*-
# !/usr/bin/env python
from pymongo import MongoClient
import random

class MongoDB(object):
    def __init__(self,collname,host,port):
        self.client = MongoClient(host,port)
        self.db = self.client.proxy
        self.collection = self.db[collname]

    def insert(self,proxy):
        '''
        :param proxy:
        :return: if the proxy is existed,return None
        '''
        if self.collection.find_one({"proxy":proxy}):
            return None
        else:
            self.collection.insert_one({"proxy":proxy})
            return True

    def pop(self):
        '''
        从数据库中随机选择一条原始代理，取出后从数据库中删除掉
        :return:数据库中无代理时返回None
        '''
        proxylist = self.getAll()
        if proxylist:
            proxy = random.choice(proxylist)
            self.delete(proxy)
            return proxy
        else:
            return None

    def get(self):
        proxylist = self.getAll()
        if proxylist:
            proxy = random.choice(proxylist)
            return proxy
        else:
            return None

    def delete(self,proxy):
        self.collection.remove({"proxy":proxy})

    def getAll(self):
        return [p["proxy"] for p in self.collection.find()]

    def delete_database(self):
        self.client.drop_database("proxy")

    def delete_collection(self):
        self.collection.drop()

if __name__ == "__main__":
    db1 = MongoDB('original_proxy','localhost',27017)
    db2 = MongoDB('useful_proxy', 'localhost', 27017)
    db1.delete_collection()
    print(db1.getAll())