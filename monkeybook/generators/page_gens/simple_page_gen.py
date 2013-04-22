from monkeybook.generators.page_gens.page_gen import PageGen

class SimplePageGen(PageGen):
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs

  def generate(self, data):
    print ('page gen is generating pages on ' + str(data) + ' with args ' + 
            str(self.args) + 'str kwargs ' + str(self.kwargs))

  def finalize(self, pages, data):
    print ('page gen is generating pages on ' + str(data) + ' with args ' + 
            str(self.args) + str(self.kwargs))

SimplePageGen.register()