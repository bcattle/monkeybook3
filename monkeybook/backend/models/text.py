from mongoengine import *

# Represents any text blocks, with alternate text blocks.

class Text(Document):
  def __init__(self):
    return
  # Example of style could be 'FacebookComment', and the frontend/template would
  # have a FacebookComment strategy or template.
  # style = StringField()
  
  text = StringField()

  width = IntegerField()
  height = IntegerField()

  photos = ListField(ReferenceField(Photo))
  text = ListField(ReferenceField(PageText))

  @property    
  def width():
    return book.width

  def height():
    return book.height