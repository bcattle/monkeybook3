#from pymongo import MongoClient
from mongoengine import *
import ipdb
def foo():
  connect('project1', 
          host='mongodb://user:pass@ds053937.mongolab.com:53937/monkeybook')
  doc = Doc()
  doc.name = 'doc'
  doc.save()
  doc2 = Doc()
  doc2.name = 'doc2'
  doc2.save()
  for doc in Doc.objects():
    print 'first ' + doc.name
  for doc in Doc.objects(name='doc'):
    print 'second ' + doc.name

class Doc(Document):
  name = StringField(required=True)
if __name__ == '__main__':
  foo()

