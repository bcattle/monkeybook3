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

    self.book_end_time = datetime.datetime(2013, 5, 1, tzinfo=utc)
    self.access_token = 'BAACEdEose0cBAEOhZB9OtuprHavggJfNU4sDq6nSjkqhbLTwC9aLUTFxX5F2GiyaoikvgqPZBTpWscodl103VhUwvHmQsiKZBBfjY0X8BpuekjQk3EYyIvckj34yFAhNOkBNa7PPqYoNCCM8EbXgTBPPbXw6O2F52NX4b6fnc29PC3oFGWlX77OOAO73ZCEdIPq5lMFdxwZDZD'
