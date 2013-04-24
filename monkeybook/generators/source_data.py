from monkeybook.data_connnectors import DataConnectors
from collections import defaultdict

class BookSourceData(object):
    def __init__(self, config):
        self.config = config
        # Set up the DataConnectors and DataProcessors
        self.data_connectors = DataConnectors()
        
        # Signals is a sparse mapping of friend/photo/comment ids to a value
        # For example
        # signals['friend_value'][friend1_id] = .75
        # signals['friend_value'][friend2_id] = .5
        # signals['friend_value'][friend3_id] = .9
        # I can now easily slice and dice this structure to get the top friends
        # sorted_friends = sorted(x.iteritems(), key=operator.itemgetter(1))
        
        self.signals = defaultdict(dict)