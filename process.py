# -*-coding:utf-8-*-
import re
import json
import requests
import time
import csv

res = re.compile(r'render_data = \[(\{.*?\"status\".*?\"hit\".*?\})',re.S)
res1 = re.compile("(.*/).*?jpg")

with open('./data.json','r') as fp:
	data = json.load(fp)
for key in data.keys():
	comment = []
	content_text = None
	create_time = None
	user_text = None
	pic_list = []

	response_key = requests.get(key)
	key_json = response_key.json()
	response_value = requests.get(data[key])

	# obtain comment
	if(len(key_json.keys()) > 2):
		comment_list = key_json['data']
		for item in comment_list:
			comment.append(item[text])

	# obtain content
	try:
		list1 = res.findall(response_value.content)[0]
		js = json.loads(list1)
	except Exception as e:
		continue

	create_time = js['status']['created_at']
	user_text = js['status']['text']

	# if the content is retweeted
	if js['status'].has_key('retweeted_status'):
		content_text = js['status']['retweeted_status']['text']
		if len(js['status']['retweeted_status']['pic_ids']) > 0:
			origin_pic = js['status']['retweeted_status']['original_pic']
			try:
				b_url = res1.findall(origin_pic)[0]
			except Exception as e:
				print js['status']['retweeted_status']
				break
			pic_list = js['status']['retweeted_status']['pic_ids']
			for i in range(len(pic_list)):
				pic_list[i] = b_url + pic_list[i] + '.jpg'
		else:
			try:
				pic_list = []
				origin_pic = js['status']['retweeted_status']['page_info']['page_pic']['url']
				pic_list.append(origin_pic)
			except Exception as e:
				pass
	else:
		if len(js['status']['pic_ids']) > 0:
			origin_pic = js['status']['original_pic']
			b_url = res1.findall(origin_pic)[0]
			pic_list = js['status']['pic_ids']
			for i in range(len(pic_list)):
				pic_list[i] = b_url + pic_list[i] + '.jpg'

	# print create_time.decode('gbk')
	# print str(user_text)
	# print comment.decode('gbk')
	# print content_text.decode('gbk')
	# print pic_list

	with open('./data.csv', 'ab') as csvfile:
	    fieldnames = ['create_time','user_text','content_text','comment','pic_list']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    # writer.writeheader()
	    writer.writerow({'create_time': create_time.encode('utf-8')})
	    writer.writerow({'user_text':user_text.encode('utf-8')})
	    if content_text == None:
	    	writer.writerow({'content_text':1234})
	    else:
	    	writer.writerow({'content_text':content_text.encode('utf-8')})

	    if len(comment) == 0:
	    	writer.writerow({'comment':[]})
	    else:
	    	writer.writerow({'comment':comment})

	    if len(pic_list) == 0:
	    	writer.writerow({'pic_list':[]})
	    else:
	    	writer.writerow({'pic_list':pic_list})
	    # break
	    # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
	    # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
	time.sleep(1)

# with open('./data.csv', 'a') as csvfile:
#     fieldnames = ['first_name', 'last_name']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     # writer.writeheader()
#     writer.writerow({'first_name': 'Baked', 'last_name': ('Beans','kerns')})
#     writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#     writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})




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