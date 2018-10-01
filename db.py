from datetime import datetime
import pymongo
import os

mongo = pymongo.MongoClient('mongodb://localhost:27017')

db = mongo['db1']
creds = db["creds"]
messages = db["messages"]
user = db["user"]


u1 = {'name': 'Mr. Shah',
      'DOB': '20-5-1960',
      'Age': '58',
      'allergies': ['peanut', 'ThyPhenol'],
      'Blood Group', 'B+',
      'visits': [
          {'date': datetime.date(11,9,18)
           'reason': 'Ankle Pain',
           'description': 'Long description on doctors analysis and conclusion',
           'medicines': ['crocin', 'metaflax']
          }
          ]
      'meds': [
          {'name': 'crocin',
            'reason': 'knee pain',
            'time': ['morning', 'afternoon']}
          ]
      }