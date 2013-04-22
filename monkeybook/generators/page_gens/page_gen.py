class PageGen(object):
  registry = {}

  @staticmethod
  def create(name, *args, **kwargs):
    return PageGen.registry[name](*args, **kwargs)

  @classmethod
  def register(cls):
    print 'registering ' + cls.__name__
    PageGen.registry[cls.__name__] = cls
    print str(PageGen.registry)

  def generate(self, data):
  	raise NotImplementedError()
  	
  def finalize(self, pages, data):
  	raise NotImplementedError()
  	
# Import all the page_gens here, theyll be automatically added to the registry.
import monkeybook.generators.page_gens.simple_page_gen
