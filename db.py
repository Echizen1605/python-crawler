import json
import datetime
from datetime import datetime
from pymongo import MongoClient

with open('data_data.json','r') as fp:
	data = json.load(fp)

data = json.loads(data)
print data.keys()

client = MongoClient()
db = client['mytest']
table = db['mytable']

for i in range(len(data['comment'])):
	dict1 = {}
	for key in data.keys():
		if key == 'create_time':
			thistime = datetime.strptime(data[key][i], "%a %b %d %H:%M:%S +0800 %Y")
			dict1[key] = thistime
		else:
			dict1[key] = data[key][i]
	table.insert_one(dict1)

client.close()

