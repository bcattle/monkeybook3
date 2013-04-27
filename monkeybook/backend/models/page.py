from mongoengine import *

from monkeybook.backend.models.photo import Image
from monkeybook.backend.models.text import PageText

# Should this be an EmbededDocument instead?
class Page(Document):
  # If this was an embedded doc, would I need a ref to the book. Are there cases
  # where a page is not embedded in a book?
  # book = ReferenceField(Book)
  # style = StringField()

  width = IntField()
  height = IntField()
  # Not sure if this is needed, or could just be impleted as photo[0]. 
  # The latter might be better since it would allow multiple resolution and 
  # alternate backgrounds.
  #background_image = StringField()

  # How are photos layered? Is it just the index of this array?
  # So bring to frint would be remove/add.
  images = ListField(EmbeddedDocumentField(Image))
  text = ListField(ReferenceField(PageText))

  # Hints for ordering the book. A page can specify an absolute page index, a 
  # a relative page index (0..1) or a next/previous page. The book orderer takes
  # previous/next page, page_index, relative_index into account in that order.
  # This value can be negative to indicate pages at the end of the book.
  # Absolte page index must be positive or negative. Not zero.
  page_index = IntField()
  relative_index = FloatField()
  previous_page = ReferenceField('Page')
  next_page = ReferenceField('Page')
  
  def __init__(self, width, height, page_index=None, relative_index=None,
               previous_page=None, next_page=None):
    super(Page, self).__init__()
    self.width = width
    self.height = height
    if page_index != None:
      self.page_index = page_index
    if relative_index != None:
      self.relative_index = relative_index
    if previous_page != None:
      self.previous_page = previous_page
    if self.next_page != None:
      self.next_page = next_page

  def add_image(self, width, height, pos_x, pos_y):
    img = Image(width, height, pos_x, pos_y)
    self.images.append(img)
    return img
    
  def __str__(self):
    index = ''
    ret = ''
    if self.relative_index:
      index += 'rel index ' + str(self.relative_index)
    if self.page_index:
      index += 'page index ' + str(self.page_index)
    if self.previous_page:
      ret += '<-'
    ret +=  '%s %d images' % (index,
                              len(self.images))
    if self.next_page:
      ret += '->'
    return ret