class Signal(object):
  registry = {}

  @staticmethod
  def create(name, *args, **kwargs):
    return Signal.registry[name](args, kwargs)

  @classmethod
  def register(cls):
    print 'registering ' + cls.__name__
    Signal.registry[cls.__name__] = cls
    print str(Signal.registry)

  def process(self, data):
    raise NotImplementedError()

# Import all the signals here, theyll be automatically added to the registry.
import monkeybook.generators.signals.simple_signal
