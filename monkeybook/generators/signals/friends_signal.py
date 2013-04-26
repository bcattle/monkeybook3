from monkeybook.generators.signals import Signal
from monkeybook.data_connnectors.results import ResultField
from monkeybook.data_connnectors.facebook.connectors import friends

# Produces a signal based on how often a friend has been tagged.
# Produces a signal [1..5]. A value of 5 is 5x stronger than a value of 1.
class TaggedFriendsSignal(Signal):
  signal_name = 'tagged_count'
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    
  def process(self, data):
    """
    This receives a
    """
    print 'processing top friends'
    # 1 point for each tag
    for photo in data.photos:
      for tag in photo.people_tagged:
        if tag.subject:
          data.friends.signals[self.signal_name][tag.subject] += 1
    
    # Normalize signal, set value in the range (1..2)
    print data.friends.signals
    vals =  data.friends.get_sorted_by_signal(self.signal_name)
    max_value = vals[0][1]
    min_value = 0
    for k, v in vals:
      data.friends.signals[self.signal_name][k] = 1.0 + 4 * float(v) / max_value
    
    print data.friends.get_sorted_by_signal(self.signal_name)
TaggedFriendsSignal.register()
