# -*- coding: utf-8 -*-
# !/usr/bin/env python

import requests
import lxml
import re
import time
from bs4 import BeautifulSoup
from bs4.element import NavigableString

headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        }

class ProxyGetter(object):
    def __init__(self):
        pass

    @staticmethod
    def _freeProxyFirst(page=10):
        '''
        抓取云代理IP http://www.ip3366.net/free/
        :param page:页数
        :return:
        '''
        print(u"正在抓取云代理IP...")
        start = time.clock()

        for num in range(1,page+1):
            url = "http://www.ip3366.net/?stype=1&page={}".format(num)
            try:
                r = requests.get(url, headers=headers, timeout=10)
                r.raise_for_status()
            except requests.RequestException as e:
                print(e)
                continue
            else:
                soup = BeautifulSoup(r.text,"lxml")
                trs = soup.find_all("tr")[1:]
                for tr in trs:
                    tds = tr.find_all("td")[:2]
                    ip = tds[0].get_text()
                    port = tds[1].get_text()
                    yield ip + ":" + port

        print(u"抓取完毕")
        end = time.clock()
        print(u"耗费的时间为%d s" % (end - start))

    @staticmethod
    def _freeProxySecond(number=10):
        '''
        抓取好IP http://haoip.cc
        :param number: 抓取页数
        :return:
        '''
        print(u"正在抓取好IP...")
        start = time.clock()

        page = 0
        url = "http://haoip.cc"
        while page < number:
            try:
                r = requests.get(url, headers=headers, timeout=10)
                r.raise_for_status()
            except requests.RequestException as e:
                print(e)
                page = page + 1
                continue
            else:
                soup = BeautifulSoup(r.text, "lxml")
                trs = soup.find_all("tr")
                nexturl = soup.find("ul",{"class":"pagination"}).li.a['href']
                for tr in trs:
                    tds = tr.find_all("td")[:2]
                    ip = tds[0].get_text()
                    port = tds[1].get_text()
                    yield ip + ":" + port
                url = "http://haoip.cc" + nexturl
                page = page + 1

        print(u"抓取完毕")
        end = time.clock()
        print(u"耗费的时间为%d s" % (end - start))

    @staticmethod
    def _freeProxyThird(number=100):
        '''
        抓取代理66 http://www.66ip.cn/
        :param number:代理数量
        :return:
        '''
        print(u"正在抓取代理66...")
        start = time.clock()

        url = "http://www.66ip.cn/nmtq.php?getnum={}&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip".format(number)
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except requests.RequestException as e:
            print(e)
            yield []
        else:
            for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', r.text):
                yield proxy
            print(u"抓取完毕")
            end = time.clock()
            print(u"耗费的时间为%d s" % (end - start))

    @staticmethod
    def _freeProxyFourth():
        '''
        抓取西刺代理 http://www.xicidaili.com/nn/
        :return:
        '''
        print(u"正在抓取西刺代理...")
        start = time.clock()

        url = "http://www.xicidaili.com/nn/"
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except requests.RequestException as e:
            print(e)
        else:
            soup = BeautifulSoup(r.text, "lxml")
            trs = soup.find_all("tr")[1:]
            for tr in trs:
                tds = tr.find_all("td")[1:3]
                ip = tds[0].get_text()
                port = tds[1].get_text()
                yield ip + ":" + port

        print(u"抓取完毕")
        end = time.clock()
        print(u"耗费的时间为%d s" % (end - start))

    @staticmethod
    def _freeProxyFifth(page=10):
        '''
        抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
        :param page:页数
        :return:
        '''
        print(u"正在抓取guobanjia...")
        start = time.clock()

        for num in range(1, page + 1):
            url = "http://www.goubanjia.com/free/gngn/index{}.shtml".format(num)
            try:
                r = requests.get(url, headers=headers)
                r.raise_for_status()
            except requests.RequestException as e:
                print(e)
                continue
            else:
                soup = BeautifulSoup(r.text, "lxml")
                tds = soup.find_all("td",{"class":"ip"})
                for td in tds:
                    str = ""
                    for child in td.children:
                        if not isinstance(child, NavigableString):
                            if child.get('style'):
                                if child['style'] is not "display:none;":
                                    if child.string:
                                        str = str + child.string
                            elif child.get('class'):
                                str = str + ":" + child.string
                    yield str

        print(u"抓取完毕")
        end = time.clock()
        print(u"耗费的时间为%d s" % (end - start))

    #作为与外部类通信的接口
    @staticmethod
    def get_free_proxy():
        #登记函数
        RegisterFunc = [
            ProxyGetter._freeProxyFirst,
            ProxyGetter._freeProxySecond,
            ProxyGetter._freeProxyThird,
            ProxyGetter._freeProxyFourth,
            ProxyGetter._freeProxyFifth
        ]

        for func in RegisterFunc:
            for proxy in func():
                yield proxy

if __name__ == '__main__':
    for proxy in ProxyGetter.get_free_proxy():
        print(proxy)