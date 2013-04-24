import datetime
from pytz import utc


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

    self.book_start_time = datetime.datetime(2012, 1, 1, tzinfo=utc)
    self.book_end_time = datetime.datetime(2013, 5, 1, tzinfo=utc)

    self.access_token = 'AAABnJj9SZBycBAEcdZAf6v1V3y4NQjOyFD8dZB590GYkIZAwHEtUHuKjTwriE4zm0mJlWH7DZB8bJy8ZAZC1dr9GT79euGCTS0ZD'
