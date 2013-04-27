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
    # This is messy needs to be cleaned up.
    print 'ordering pages'
    print pages
    starting_pages = pages
    starting_len = len(pages)
    # Set aside pages with previous_page (rel_index, positive page_index) and next_page (negative page_index)
    # assert 1 page with positive index and no previous_page
    # page 1, and other next page
    # relative pages next
    # next pages after that
    # assumes only one set of beginning and ending pages, everything else is relative.
    last_page = None
    first_page = None
    relative_pages = []
    for page in pages:
      if page.page_index != None and page.page_index > 0 and not page.previous_page:
        assert not first_page, 'Ambigious first pages %s %s' % (first_page, page)
        print 'first page found ' + str(page)
        first_page = page
        
      if page.page_index != None and page.page_index < 0 and not page.previous_page:
        assert not last_page, 'Ambigious last pages %s %s' % (last_page, page)
        print 'last page found (sort of) ' + str(page)
        last_page = page
      
      if page.relative_index and not page.previous_page:
        print 'adding relative page ' + str(page)
        relative_pages.append(page)
    
    relative_pages.sort(key=lambda p: p.relative_index)
    
    pages = [first_page] + relative_pages + [last_page]
    final_pages = []
    for page in pages:
      while page:
        final_pages.append(page)
        page = page.next_page
    print 'final ' + str(final_pages)
        
    assert starting_len == len(final_pages), 'page count mismatch'
    return final_pages
    
def main():
  print 'Starting up'
  
  simple_config = BookGeneratorConfig()
  simple_config.signals.append(Signal.create('TaggedFriendsSignal', 7, 8, 9, foo='bar'))
  simple_config.signals.append(Signal.create('PhotoAgeSignal', 7, 8, 9, foo='bar'))
  simple_config.signals.append(Signal.create('PhotoCommentsLikesSignal', 7, 8, 9, foo='bar'))
  simple_config.signals.append(Signal.create('PhotoTagsSignal', 7, 8, 9, foo='bar'))
  simple_config.signals.append(Signal.create('PhotoSumSignal', 7, 8, 9, foo='bar'))
  

  simple_config.page_gens.append(PageGen.create('StaticPageGen', width=100, 
                                                page_index = 1, height=100, 
                                                background_images=['c0', 'c1', 'c2', 'c3']))

  simple_config.page_gens.append(PageGen.create('StaticPageGen', width=100, 
                                                page_index = -1, height=100, 
                                                background_images=['b0', 'b1', 'b2', 'b3']))
                                                
  simple_config.page_gens.append(PageGen.create('StaticPageGen', width=100, 
                                                relative_index = .5, height=100, 
                                                background_images=['s.50', 's.51', 's.52', 's.53']))
                                                
  for i in xrange(8):
    relative = (i + 1) / float(10)
    simple_config.page_gens.append(PageGen.create('StaticPageGen', width=100, 
                                                  relative_index = relative, height=100, 
                                                  background_images=[str(i)+'0']))
                                                
                                                

                                                
  simple_config.page_gens.append(PageGen.create('SimplePageGen', 1, 2))
  simple_config.page_gens.append(PageGen.create('SimplePageGen', 3, 4, foo2='bar2'))

  gen = BookGenerator(simple_config)

  data = SchoolYearbook2013SourceData(simple_config)
  data.collect_data()

  gen.generate_book(data)

if __name__ == '__main__':
  main()
