
class ResultStorage(object):
    def __init__(self):
        pass

    def store(self, query_type, query, results):
        raise NotImplementedError

    def retrieve(self, query):
        raise NotImplementedError
