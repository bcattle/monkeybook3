from monkeybook.generators.signals import Signal
from monkeybook.generators.signals.friends_signal import TaggedFriendsSignal
from monkeybook.data_connnectors.results import ResultField
from monkeybook.data_connnectors.facebook.connectors import friends
import datetime
import pytz


# The number of comments and likes on the photo
# Signal is between [1..5]. 1 is one comment/like 5 is 20 comments or 40 likes (2*comments+likes)/40
# comments are values 2x than likes
class PhotoCommentsLikesSignal(Signal):
  signal_name = 'comments_likes_count'
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    
  def process(self, data):
    """
    This receives a
    """
    print 'processing photos'
    # Sum all friends
    for photo in data.photos:
      comment_count = photo.comment_info['comment_count']
      like_count = photo.like_info['like_count']
      # maximum value should be based of median of top N values
      if comment_count == 0 and like_count == 0:
        normalized_value = 0
      else:
        normalized_value = ((comment_count * 2 + like_count) / float(40)) * 4 + 1
      
      data.photos.signals[self.signal_name][photo.id] = normalized_value
    
    vals =  data.photos.get_sorted_by_signal(self.signal_name)
    print vals[:10]
    
# The sum of other photos, producing the final ranking. 
# Probably should be parameterized by the signals to sum
class PhotoAgeSignal(Signal):
  signal_name = 'photo_age'
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    
  def process(self, data):
    """
    This receives a
    """
    print 'processing photos'
    # Sum all friends
    for photo in data.photos:
      delta_days = max(0, (datetime.datetime.now(pytz.utc) - photo.created).days)
      # Normalized over 5 years.
      val = max(0, 5 * (1 - delta_days / float(365 * 5)))
      data.photos.signals[self.signal_name][photo.id] = val
    
    vals =  data.photos.get_sorted_by_signal(self.signal_name)
    print vals[:10]
    

# The age of the photo
# Signal is between [0..5]. 0 is 5 years ago, 5 is recent.
# comments are values 2x than likes
class PhotoSumSignal(Signal):
  signal_name = 'photo_sum'
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    
  def process(self, data):
    """
    This receives a
    """
    print 'processing photos'
    # Sum all friends
    signals = [PhotoTagsSignal, PhotoCommentsLikesSignal, PhotoAgeSignal]
    for photo in data.photos:
      val = 0
      for signal in signals:
        val += data.photos.signals[signal.signal_name][photo.id]
      data.photos.signals[self.signal_name][photo.id] = val
    
    vals =  data.photos.get_sorted_by_signal(self.signal_name)
    print vals[:10]


# The sum of all friends tagged values.
class PhotoTagsSignal(Signal):
  signal_name = 'tag_values'
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    
  def process(self, data):
    """
    This receives a
    """
    print 'processing photos'
    data.friends.get_sorted_by_signal(TaggedFriendsSignal.signal_name)
    # Sum all friends
    for photo in data.photos:
      for tag in photo.people_tagged:
        if tag.subject:
          data.photos.signals[self.signal_name][photo.id] += (
            data.friends.signals[TaggedFriendsSignal.signal_name][tag.subject])
    
    vals =  data.photos.get_sorted_by_signal(self.signal_name)
    print vals[:10]
    
class TopPhotosSignal(Signal):
    def __init__(self, *args, **kwargs):
        pass

    def process(self, data):
        pass


class GroupPhotosSignal(Signal):
    def __init__(self, *args, **kwargs):
        pass

    def process(self, data):
        pass

PhotoSumSignal.register()
PhotoTagsSignal.register()
PhotoCommentsLikesSignal.register()
PhotoAgeSignal.register()