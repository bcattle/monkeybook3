import ipdb
from monkeybook.generators.signals.signal import Signal
from monkeybook.generators.page_gens.page_gen import PageGen

class BookGeneratorConfig(object):
  def __init__(self):
    # Ideally this should be built from some sort of config file
    self.signals = []
    self.page_gens = []
    self.width = 1000
    self.height = 1000

    # I'm ignoring tracking odd and even pages for now.
    self.target_pages = 50
    self.max_pages = 75


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
  simple_config.signals.append(Signal.create('SimpleSignal', 7, 8, 9, foo='bar'))

  simple_config.page_gens.append(PageGen.create('StaticPageGen', 1, width=100, height=100, img='static_img.jpg'))
  simple_config.page_gens.append(PageGen.create('SimplePageGen', 1, 2))
  simple_config.page_gens.append(PageGen.create('SimplePageGen', 3, 4, foo2='bar2'))

  gen = BookGenerator(simple_config)
  gen.generate_book([])

if __name__ == '__main__':
  main()
