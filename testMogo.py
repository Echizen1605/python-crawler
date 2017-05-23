import json
from datetime import datetime
from pymongo import MongoClient

client = MongoClient()
db = client['mytest']
table = db['mytable']

for item in table.find({'create_time':{'$gte':datetime(2014,12,28),'$lt':datetime(2015,1,3)}}):
	print item['url']
