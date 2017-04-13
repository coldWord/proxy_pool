# -*- coding: utf-8 -*-
# !/usr/bin/env python
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import sys
import threading

sys.path.append('../')

from DB.mongoDBCilent import MongoDB
from ProxyGetter.getfreeproxy import ProxyGetter

class Manager(object):
    def __init__(self):
        self.headers = {'Connection': 'keep-alive',
                   'Cache-Control': 'max-age=0',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   }
        self.origin = MongoDB('original_proxy', 'localhost', 27017)
        self.useful = MongoDB('useful_proxy', 'localhost', 27017)

    def _isProxy(self,proxy):
        '''
        检查代理格式
        :param proxy:
        :return:
        '''
        import re
        vaildProxy = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
        return True if re.match(vaildProxy, proxy) else False

    def _validUsefulProxy(self, proxy):
        """
        检验代理可用性
        :param proxy:
        :return:
        """
        if self._isProxy(proxy):
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告
            proxies = {"http": "http://{proxy}".format(proxy=proxy),
                       "https":"http://{proxy}".format(proxy=proxy)}
            try:
                # 超过20秒的代理就不要了
                r = requests.get('https://www.baidu.com/', proxies=proxies, timeout=20, verify=False, headers=self.headers)
                if r.status_code == 200:
                    print("Useful")
                    return True
            except requests.RequestException as e:
                print(e)
                return False
        else:
            return False

    def run(self):
        print(u"开始运行程序")
        for proxy in ProxyGetter.get_free_proxy():
            self.origin.insert(proxy)

        print(u"开始验证")
        for i in range(1,10):
            t = threading.Thread(target=self.vaild)
            t.start()
        
    def vaild(self):
        while True:
            proxy = self.origin.pop()
            if proxy:
                if self._isProxy(proxy):
                    if self._validUsefulProxy(proxy):
                        self.useful.insert(proxy)
            else:
                print(u"代理验证结束")
                break

    def refresh(self):
        '''
        对useful_proxy数据库中的代理进行再次验证
        :return:
        '''
        proxylist = self.useful.getAll()
        if proxylist:
            for proxy in proxylist:
                if not self._validUsefulProxy(proxy):
                    self.useful.delete(proxy)
            proxylist = self.useful.getAll()
            if not proxylist:
                self.run()
        else:
            self.run()

if __name__ == "__main__":
    ma = Manager()
    #ma.run()
    ma.refresh()
