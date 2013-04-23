from monkeybook.data_connnectors import DataConnectors


class BookSourceData(object):
    def __init__(self, config):
        self.config = config
        # Set up the DataConnectors and DataProcessors
        self.data_connectors = DataConnectors()
