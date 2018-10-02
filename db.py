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
      'allergies': 'peanuts, ThyPhenol',
      'Blood Group': 'B+',
      'visits': [
          {'date': '11-8-2018',
           'reason': 'Ankle Pain',
           'description': 'Long description on doctors analysis and conclusion',
           'medicines': ['crocin', 'metaflax'],
           'future': 'false',
           'cost': '800',
           'txn': 'abcd'
          },
          {'date': '18-7-2018',
           'reason': 'Stomach Upset',
           'description': 'Long description on doctors analysis and conclusion',
           'medicines': ['Roflax'],
           'future': 'false',
           'cost': '760',
           'txn': 'asas'
          },
          {'date': '1-1-2018',
           'reason': 'Cataract Surgery',
           'description': 'Long description on doctors analysis and conclusion',
           'medicines': ['Roflax'],
           'future': 'false',
           'cost': '13000',
           'txn': 'axax'
          },

          ],
      'meds': 
         [ {'name': 'RolFlax','reason': 'knee pain', 'time': 'night'},
                    {'name':'crocin', 'reason':'fever', 'time':'night'}]

      
    
      }
user.delete_one({'username':'darsh'})
user.insert_one(u1)