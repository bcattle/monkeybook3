from mongoengine import *

# Represents any text blocks, with alternate text blocks.

class PageText(Document):
  def __init__(self):
    return
  # Example of style could be 'FacebookComment', and the frontend/template would
  # have a FacebookComment strategy or template.
  # style = StringField()
  
  text = StringField()

  width = IntField()
  height = IntField()
