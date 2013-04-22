from monkeybook.generators.signals import Signal

class SimpleSignal(Signal):
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs

  def process(self, data):
    print ('signal is processing data ' + str(data) + ' with args ' + 
            str(self.args) + str(self.kwargs))

SimpleSignal.register()
