from mongoengine import *
from monkeybook.backend.models.text import PageText

# A contains information about an image to display in the photobook.
class Image(EmbeddedDocument):
  
  # The width and height on the page
  width = IntField()
  height = IntField()
  pos_x = IntField()
  pos_y = IntField()
  
  primary_photo = ReferenceField('Photo')
  alternate_photos = ListField(ReferenceField('Photo'))
  

class Photo(Document):
  def __init__(self):
    return

  # style = StringField()
  
  # The actual resolution of the photo
  text = ListField(ReferenceField(PageText))
  urls = ListField(EmbeddedDocumentField('PhotoUrl'))

class PhotoUrl(EmbeddedDocument):
  url = StringField()
  width = IntField()
  height = IntField()
