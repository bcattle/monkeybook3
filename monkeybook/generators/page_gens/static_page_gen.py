from monkeybook.generators.page_gens.page_gen import PageGen
from monkeybook.backend.models.page import Page
from monkeybook.backend.models.photo import Image
from monkeybook.backend.models.photo import Photo

class StaticPageGen(PageGen):
  def __init__(self, *args, **kwargs):
    self.width = kwargs.pop('width')
    self.height = kwargs.pop('height')
    # used for multiple page spreads.
    self.background_images = kwargs.pop('background_images', None)
    self.page_index = kwargs.pop('page_index', None)
    self.relative_index = kwargs.pop('relative_index', None)
    
    
    self.args = args
    self.kwargs = kwargs

  def generate(self, data):
    print ('static page gen is generating pages on ' + str(data) + ' with args ' + 
            str(self.args) + 'str kwargs ' + str(self.kwargs) + 'width ' + str(self.width))
      
    pages = []
    previous_page = None
    for background_image in self.background_images:
      page = Page(self.width, self.height, page_index=self.page_index, 
                  relative_index=self.relative_index)
      if previous_page:
        page.previous_page = previous_page
        previous_page.next_page = page
      img = page.add_image(self.width-20, self.height-20, 10, 10)
      img.primary_photo = Photo(background_image)
      pages.append(page)
      previous_page = page
      print str(page)
      
    return pages
  

  def finalize(self, pages, data):
    print ('page gen is generating pages on ' + str(data) + ' with args ' + 
            str(self.args) + str(self.kwargs))

StaticPageGen.register()