from datetime import datetime
import pymongo
import os

mongo = pymongo.MongoClient('mongodb://localhost:27017')

db = mongo['db1']
creds = db["creds"]
messages = db["messages"]
user = db["user"]


u1 = {'name': 'Ms. Shah',
      'username': 'darsh',
      'pin': 'darsh',
      'DOB': '20-5-1960',
      'Age': '58',
      'allergies': ['peanut', 'ThyPhenol'],
      'Blood Group': 'B+',
      'visits': [
          {'date': '11-8-2018',
           'reason': 'Ankle Pain',
           'description': 'Long description on doctors analysis and conclusion',
           'medicines': ['crocin', 'metaflax']
          }
          ],
      'medtime': {
          'night':  [{'name': 'RolFlax','reason': 'knee pain'}]

      }
      
      
      
    
      }