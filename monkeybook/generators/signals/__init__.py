class Signal(object):
  registry = {}

  @staticmethod
  def create(name, *args, **kwargs):
    return Signal.registry[name](*args, **kwargs)

  @classmethod
  def register(cls):
    print 'registering ' + cls.__name__
    Signal.registry[cls.__name__] = cls
    print str(Signal.registry)

  def process(self, data):
    raise NotImplementedError()


# Import all the signals here, they'll be automatically added to the registry.
import simple_signal
