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
  page_index = IntField()
  relative_index = FloatField()
  previous_page = ReferenceField('Page')
  next_page = ReferenceField('Page')

  def add_photo():
    return