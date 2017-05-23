import re
import json
import requests
import time
import csv
import codecs
import os
import os.path
from multiprocessing import Process,Queue,Pool
import multiprocessing
import random

import gevent
from gevent import monkey
monkey.patch_all()

headers={
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate, sdch, br",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive",
	"Host":"m.weibo.cn",
	"Upgrade-Insecure-Requests":"1"
}

user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
              'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
              'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
              'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30']
# headers = {"User-Agent": "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0"}

with open('./ip.json','r') as fp:
	proxylist = json.load(fp)
proxy_key = proxylist.keys()


with open('./data1.json','r') as fp:
	data = json.load(fp)

urllist = []
depletelist = []


for key in data.keys():
	urllist.append((key,data[key]))
urllist = urllist[:20]

proxy = {}

def fetch(key_value):
	time.sleep(4)
	key = key_value[0]
	value = key_value[1]
	try:
		random_proxy_key = random.choice(proxy_key)
		proxy[proxylist[random_proxy_key][0]] = proxylist[random_proxy_key][1]

		headers['User-Agent'] = random.choice(user_agent)
		response_key = requests.get(key,headers=headers,proxies=proxy)
		print key
		response_key.close()
		response_value = requests.get(value,headers=headers,proxies=proxy)
		print value
		response_value.close()
	except Exception as e:
		depletelist.append((key,value))

gevent_list = [gevent.spawn(fetch,key_value) for key_value in urllist]
for item in gevent_list:
	item.join()

# for item in urllist:
# 	fetch(item)

print len(depletelist)






# https://my.oschina.net/yangyanxing/blog/296052
