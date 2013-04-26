from monkeybook.generators.schoolyearbook2013.config import BookGeneratorConfig
from monkeybook.generators.schoolyearbook2013.source_data import SchoolYearbook2013SourceData
from monkeybook.generators.signals import Signal
from monkeybook.generators.page_gens.page_gen import PageGen


class BookGenerator(object):
  # Global registries for signals and page_gens
  signal_registry = {}
  page_gen_registry = {}
  def __init__(self, config):
    print 'initializing book generator w/ config ' + str(config)
    self.config = config
    
  
  def generate_book(self, data):
    print 'generating book with data ' + str(data)
    pages = []
    # Preprocess
    for signal in self.config.signals:
      signal.process(data)

    # Process
    for page_gen in self.config.page_gens:
      new_pages = page_gen.generate(data)
      if new_pages:
        pages.extend(new_pages)

    pages = self.order_pages(pages)

    # Postprocess
    for page_gen in self.config.page_gens:
      page_gen.finalize(pages, data)

  def save_book(self):
    print 'saving book'

  def order_pages(self, pages):
    print 'ordering pages'
    return pages

def main():
  print 'Starting up'
  
  simple_config = BookGeneratorConfig()
  simple_config.signals.append(Signal.create('SimpleSignal', 1, 2, 3))
  simple_config.signals.append(Signal.create('SimpleSignal', 4, 5, 6))
  simple_config.signals.append(Signal.create('TaggedFriendsSignal', 7, 8, 9, foo='bar'))

  simple_config.page_gens.append(PageGen.create('StaticPageGen', 1, width=100, 
                                                height=100, img='static_img.jpg'))
  simple_config.page_gens.append(PageGen.create('SimplePageGen', 1, 2))
  simple_config.page_gens.append(PageGen.create('SimplePageGen', 3, 4, foo2='bar2'))

  gen = BookGenerator(simple_config)

  data = SchoolYearbook2013SourceData(simple_config)
  data.collect_data()

  gen.generate_book(data)

if __name__ == '__main__':
  main()
