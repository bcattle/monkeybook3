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
  
  
  def __init__(self, width, height, pos_x, pos_y):
    super(Image, self).__init__()
    self.width = width
    self.height = height
    self.pos_x = pos_x
    self.pos_y = pos_y
  
class Photo(Document):
  def __init__(self, url, width=0, height=0):
    super(Photo, self).__init__()
    self.add_url(url, width, height)
  # style = StringField()
  
  # The actual resolution of the photo
  text = ListField(ReferenceField(PageText))
  urls = ListField(EmbeddedDocumentField('PhotoUrl'))
  
  def add_url(self, url, width=0, height=0):
    self.urls.append(PhotoUrl(url, width, height))    

class PhotoUrl(EmbeddedDocument):
  url = StringField()
  width = IntField()
  height = IntField()
  def __init__(self, url, width, height):
    super(PhotoUrl, self).__init__()
    self.width = width
    self.height = height
    self.url = url
    
