from mongoengine import *

# A contains information about an image to display in the photobook.
# It has all the resolutions of the image, any alternate photos, and possibly
# any associated comments. 
class Photo(Document):
  def __init__(self):
    return

  style = StringField()
  
  width = IntegerField()
  height = IntegerField()

  pos_x = IntegerField()
  pos_y = IntegerField()

  text = ListField(ReferenceField(Text))
  images = ListField(ReferenceField(Image))
  alt_photos = ListField(ReferenceField(Photo))

  @property    
  def width():
    return book.width

  @property
  def height():
    return book.height

  @property
  def image():
    # return the largest image
    return

class Image(EmbededDocument):
  url = StringField()
  # The native width/height of the image, not the width height on the page.
  width = IntegerField()
  height = IntegerField()
