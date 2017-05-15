import json
import csv
with open('data_data.json','r') as fp:
	data = json.load(fp)
data = json.loads(data)
print data.keys()
print len(data['comment'])

with open('data1.csv','w') as fp:
	fieldnames = ['create_time','user_text','content_text','comment','pic_list']
	writer = csv.DictWriter(fp, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(30):
		for key in data.keys():
			if type(data[key][i]) != list:
				if data[key][i] != None:
					writer.writerow({key:data[key][i].encode('utf-8')})
			else:
				writer.writerow({key:data[key][i]})