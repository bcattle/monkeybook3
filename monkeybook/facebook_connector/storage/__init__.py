from .mongodb import FqlResult


class ResultStorage(object):
    def __init__(self):
        pass

    def store(self, query_type, query, results):
        raise NotImplementedError

    def retrieve(self, query):
        raise NotImplementedError


class MongoQueryStorage(ResultStorage):
    """
    A connector to the `FqlResults` collection in the db
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def store(self, query_type, query, results):
        """
        Stores the results of a FQL query to the database
        """
        fql_result = FqlResult(
            user_id = self.user_id,
            query_type = query_type,
            query = query,
            results = results
        )
        fql_result.save()

    def retrieve(self, query):
        return FqlResult.objects.first(user_id=self.user_id, query=query).results

