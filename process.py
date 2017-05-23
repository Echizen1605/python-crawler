# -*-coding:utf-8-*-
import re
import json
import requests
import time
import csv
import codecs
import os
import os.path

res = re.compile(r'render_data = \[(\{.*?\"status\".*?\"hit\".*?\})',re.S)

with open('./data1.json','r') as fp:
	data = json.load(fp)

dict1 = {'url':[],'comment':[],'content_text':[],'create_time':[],'user_text':[],'pic_list':[]}

count = 1

for key in data.keys():
	if count < 495:
		count += 1
		continue
	comment = []
	content_text = None
	create_time = None
	user_text = None
	pic_list = []

	try:
		response_key = requests.get(key)
		response_value = requests.get(data[key])
	except Exception as e:
		print str(count) + " No0"
		count += 1
		print data[key]
		continue
	try:
		key_json = response_key.json()
	except Exception as e:
		print str(count) + "error"
		count += 1
		print data[key]
		continue

	# obtain comment
	if(len(key_json.keys()) > 2):
		comment_list = key_json['data']
		for item in comment_list:
			comment.append(item['text'])

	# obtain content
	try:
		list1 = res.findall(response_value.content)[0]
		js = json.loads(list1)
	except Exception as e:
		print str(count) + " No1"
		count += 1
		print data[key]
		continue

	try:
		create_time = js['status']['created_at']
		user_text = js['status']['text']
	except Exception as ex:
		print str(count) + " NoNo"
		count += 1
		print data[key]
		continue

	if js['status'].has_key('retweeted_status'):
		print str(count) + " retweeted"
		count += 1
		continue


	# if the content is retweeted
	if js['status'].has_key('retweeted_status'):
		try:
			content_text = js['status']['retweeted_status']['text']
			if js['status']['retweeted_status'].has_key('pic_ids'):
				if len(js['status']['retweeted_status']['pic_ids']) > 0:
					origin_pic = js['status']['retweeted_status']['original_pic']
					try:
						# b_url = res1.findall(origin_pic)[0]
						suffix = os.path.splitext(origin_pic)[1]
						b_url = os.path.split(os.path.splitext(origin_pic)[0])[0]
					except Exception as e:
						print js['status']['retweeted_status']
						break
					pic_list = js['status']['retweeted_status']['pic_ids']
					for i in range(len(pic_list)):
						pic_list[i] = b_url + "/" + pic_list[i] + suffix
				else:
					try:
						pic_list = []
						origin_pic = js['status']['retweeted_status']['page_info']['page_pic']['url']
						pic_list.append(origin_pic)
					except Exception as e:
						pass
		except Exception as ex:
			print str(count) + " No2"
			print data[key]
			count += 1
			break
	else:
		try:
			if len(js['status']['pic_ids']) > 0:
				origin_pic = js['status']['original_pic']
				suffix = os.path.splitext(origin_pic)[1]
				b_url = os.path.split(os.path.splitext(origin_pic)[0])[0]
				# b_url = res1.findall(origin_pic)[0]
				pic_list = js['status']['pic_ids']
				for i in range(len(pic_list)):
					pic_list[i] = b_url + "/" + pic_list[i] + suffix
		except Exception as ex:
			print str(count) + " No3"
			print data[key]
			count += 1
			continue

	dict1['url'].append(data[key])
	dict1['comment'].append(comment)
	dict1['content_text'].append(content_text)
	dict1['create_time'].append(create_time)
	dict1['user_text'].append(user_text)
	dict1['pic_list'].append(pic_list)

	print str(count) + " OK"
	count += 1
	time.sleep(1)

with open('data_data.json','a') as fp:
	json.dump(json.dumps('dict1'), fp)