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
           'description': 'Allow Opiods for pain. PT Ankle Hairline Crack',
           'medicines': ['crocin', 'metaflax'],

           'cost': '800',
           'txn': '12198462167264047'
          },
          {'date': '18-7-2018',
           'reason': 'Stomach Upset',
           'description': 'Food Poisoning, RMT Blood R-Cell LOW',
           'medicines': ['Roflax'],

           'cost': '760',
           'txn': '16198462167264047'
          },
          {'date': '1-1-2018',
           'reason': 'Cataract Surgery',
           'description': 'Long description on doctors analysis and conclusion',
           'medicines': ['Roflax'],

           'cost': '13000',
           'txn': '16198432167264047'
          },

          ],
      'meds': 
         [ {'name': 'RolFlax','reason': 'knee pain', 'time': 'afternoon'},
                    {'name':'crocin', 'reason':'fever', 'time':'afternoon'}]

      
    
      }
user.delete_one({'username':'darsh'})
user.delete_one({'username':'doctor'})
user.insert_one({'username':'doctor', 'pin':'doctor'})
user.insert_one(u1)