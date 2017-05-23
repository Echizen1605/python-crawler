import requests
import gevent
import time
from bs4 import BeautifulSoup
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()
import json

# proxy = {
# 	"http":"http//60.167.20.38:808",
# 	"https":"https//1.195.124.131:808"
# }

headers = {
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Host":"www.xicidaili.com",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	"Accept-Encoding":"gzip, deflate, sdch"
}

header={
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate, sdch, br",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive",
	"Host":"m.weibo.cn",
	"Upgrade-Insecure-Requests":"1"
}

def getIp():
	url = "http://www.xicidaili.com/nn/"
	data = []
	for i in range(1,30):
		tempurl = url + str(i)
		response = requests.get(tempurl,headers=headers)
		soup = BeautifulSoup(response.content, 'lxml')
		table = soup.find_all(id = "ip_list")[0]
		for tr in table.find_all("tr"):
			td = tr.find_all("td")
			if len(td) > 0:
				str1 = str(td[5].text).lower() +"://"+str(td[1].text)+":"+str(td[2].text)
				data.append(str1)
		time.sleep(3)
	return data

data = getIp()

print len(data)
iplist = []


def testIp(url):
	proxy = {}
	if url[4] == 's':
		proxy['https'] = url
	else:
		proxy['http'] = url
	try:
		# response = requests.get('http://1212.ip138.com/ic.asp',proxies=proxy)
		response = requests.get('http://m.weibo.cn/status/EFgEYemBI?mblogid=EFgEYemBI&luicode=10000011&lfid=1076033306284447&featurecode=20000180',proxies=proxy,headers=header,timeout=2)
		if len(response.content) > 2000:
			print url
			iplist.append(url)
	except Exception as ex:
		pass

if __name__ == '__main__':
	pool = Pool(20)
	pool.map(testIp, data)
	count = 0
	dictip = {}
	for ip in iplist:
		if ip[4] == 's':
			temptuple = tuple(('https',ip))
		else:
			temptuple = tuple(('http',ip))
		dictip[count] = temptuple
		count += 1

	print len(dictip.keys())
	with open('ip.json','w') as fp:
		json.dump(json.loads(json.dumps(dictip)),fp)





