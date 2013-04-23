from mongoengine import *

class Book(Document):
  def __init__(self):
    super(Book, self).__init__()

# Initial version of the 'dumb' book. The only thing in the model is information
# that is needed to edit and display the book. Additional information, such as
# rankings is not kept in the book.
#
# The goal is to make this model as simple as possible and have it be an easily
# manipulated data structure for the generator to produce and the front end to 
# consume.
#
# Right now the book is barebones and additional fields will be uncommented or
# added later.
class Book(Document):
  # Optional hints for the template rendering the book. For example, the name
  # of the template, config, or css to use to render the book.
  # Commented out for now until we figure out a use case for it.
  #style = StringField()
  
  # All pages in the book have the same width and height. These values are
  # mostly so elements in a page have a max_width and max_height. The front
  # end may scale this as necessary. For example, a book can have width=200, 
  # height = 100, with photos being 50 wide. THe front end may scale that to 
  # 1000 height and the photos would then be 500 height.
  width = IntegerField()
  height = IntegerField()

  # Note: The cover is page 1 of the book. There is no explicit cover page
  # field. If needed we can add a front_cover and back_cover field.
  pages = ListField(ReferenceField(Page))
  owner = ReferenceField(User, required=True)
  # created = DateTimeField(default=lambda: datetime.datetime.utcnow())
  # run_time = FloatField()

  