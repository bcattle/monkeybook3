from monkeybook.generators.page_gens.page_gen import PageGen
from monkeybook.backend.models.page import Page

class StaticPageGen(PageGen):
  def __init__(self, *args, **kwargs):
    self.width = kwargs.pop('width')
    self.height = kwargs.pop('height')
    self.background_image = kwargs.pop('img')
    
    self.args = args
    self.kwargs = kwargs

  def generate(self, data):
    print ('static page gen is generating pages on ' + str(data) + ' with args ' + 
            str(self.args) + 'str kwargs ' + str(self.kwargs) + 'width ' + str(self.width))
    
    pages = []
    page = Page()

  def finalize(self, pages, data):
    print ('page gen is generating pages on ' + str(data) + ' with args ' + 
            str(self.args) + str(self.kwargs))

StaticPageGen.register()