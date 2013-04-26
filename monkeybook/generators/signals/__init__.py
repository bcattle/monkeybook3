
class Signal(object):
  registry = {}

  @classmethod
  def register(cls):
    print 'registering ' + cls.__name__
    Signal.registry[cls.__name__] = cls

  @staticmethod
  def create(name, *args, **kwargs):
    return Signal.registry[name](*args, **kwargs)

  # This does not directly have references to the
  # `DataConnectors` or `DataProcessors` objects

  # Rather, those are called first then the data
  # class that they generate is passeed to the signals

  # Should the references be embedded directly here?

  def process(self, data):
    raise NotImplementedError()


# Import all the signals here, they'll be automatically added to the registry.
import simple_signal
import friends_signal
import photos_signal