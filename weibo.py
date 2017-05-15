import requests
from bs4 import BeautifulSoup
import time
import json

url = "https://m.weibo.cn/api/container/getIndex?uid=3306284447&luicode=10000011&lfid=100103type%3D3%26q%3D%E6%9C%ACgirl%E6%98%AF%E5%8D%83%E7%BA%B8%E9%B9%A4&featurecode=20000180&type=uid&value=3306284447&containerid=1076033306284447"
# url = "https://m.weibo.cn/api/container/getIndex?containerid=2304133260141131_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03"
base_url = "http://m.weibo.cn/api/comments/show?id="
dict1 = {}
page = 1
count = 0


thecount = 0
while(True):
	# if page == None:
	# 	break
	if page > 100:
		break

	print page

	response = requests.get(url+'&page='+str(page), verify = False)
	myjson = response.json()
	# page = myjson['cardlistInfo']['page']
	page += 1
	mylist = myjson['cards']

	for item in mylist:
		if str(item['itemid']) == "":
			continue
		myid = str(item['itemid'].split("_-_")[1])
		key = base_url + myid + "&page=1"
		value = str(item['scheme'])
		dict1[key] = value
		print value
	time.sleep(1)

js = json.loads(json.dumps(dict1))
with open('data1.json','wb') as fp:
	json.dump(js, fp)