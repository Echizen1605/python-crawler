import requests
from bs4 import BeautifulSoup
import pdb

# url = "http://m.weibo.cn/?&jumpfrom=weibocom"
# url1 = "http://m.weibo.cn/u/3306284447?uid=3306284447&luicode=10000011&lfid=100103type%3D3%26q%3D%E6%9C%ACgirl%E6%98%AF%E5%8D%83%E7%BA%B8%E9%B9%A4&featurecode=20000180"
# code = 'ISO-8859-1'

# html = requests.session().get(url1, headers=headers)


# http://m.weibo.cn/api/comments/show?id=4104053027752045&page=1
# http://m.weibo.cn/api/comments/show?id=4095819998846116&page=1

# http://m.weibo.cn/api/comments/show?id=4071088226907933&page=1

# javascript:;

url = "https://m.weibo.cn/api/container/getIndex?uid=3306284447&luicode=10000011&lfid=100103type%3D3%26q%3D%E6%9C%ACgirl%E6%98%AF%E5%8D%83%E7%BA%B8%E9%B9%A4&featurecode=20000180&type=uid&value=3306284447&containerid=1076033306284447"
# url = "https://m.weibo.cn/api/container/getIndex?containerid=2304133260141131_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03"
base_url = "http://m.weibo.cn/api/comments/show?id="
dict1 = {}
page = 1
count = 0

# pdb.set_trace()

thecount = 0
while(True):

	# pdb.set_trace()
	if thecount > 20:
		break
	if page == None:
		break
	response = requests.get(url+'&page='+str(page))
	myjson = response.json()
	page = myjson['cardlistInfo']['page']
	mylist = myjson['cards']

	# pdb.set_trace()

	for item in mylist:
		if str(item['itemid']) == "":
			continue
		myid = str(item['itemid'].split("_-_")[1])
		key = base_url + myid + "&page=1"
		value = str(item['scheme'])
		# dict1[count] = tuple((key, value))
		dict1[key] = value
		# count += 1
		print value
		thecount += 1

print dict1

# import re
# import json
# response = requests.get('http://m.weibo.cn/status/EFnGhhL2M?mblogid=EFnGhhL2M&luicode=10000011&lfid=1076033306284447&featurecode=20000180').content
# res = re.compile('render_data = \[({.*?\"status\".*?\"hit\".*?})',re.S)
# list1 = res.findall(response)[0]
# js = json.loads(list1)

# create_time = js['status']['created_at']
# user_text = js['status']['text']
# if js['status'].has_key('retweeted_status'):
# 	content_text = js['status']['retweeted_status']['text']
# 	if js['status']['retweeted_status'].has_key('page_info'):
# 		content_pic = js['status']['retweeted_status']['page_info']['page_pic']['url']
# else:
# 	if js['status'].has_key('pic_ids'):
# 		origin_pic = js['status']['original_pic']
# 		res1 = re.compile("(.*/).*?jpg")
# 		b_url = res1.findall(origin_pic)[0]
# 		pic_list = js['status']['pic_ids']
# 		for i in range(len(pic_list)):
# 			pic_list[i] = b_url + pic_list[i] + ".jpg"



