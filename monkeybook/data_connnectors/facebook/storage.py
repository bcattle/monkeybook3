import datetime
from monkeybook.data_connnectors.storage import ResultStorage
from mongoengine import *


class MongoQueryStorage(ResultStorage):
    """
    A connector to the `FqlResults` collection in the db
    """
    def __init__(self, user_id):
        self.user_id = user_id
        super(MongoQueryStorage, self).__init__()

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


class FqlResult(Document):
    """
    Holds the results of an individual FQL query
    run for a user
    """
    user_id = StringField(max_length=30, required=True)
    created = DateTimeField(default=lambda: datetime.datetime.utcnow())
    query_type = StringField(max_length=20, required=True)
    query = StringField(max_length=1000, required=True)
    results = DynamicField(required=True)

    meta = {
        'indexes': ['user_id', ('user_id', 'query_type'), ('user_id', 'query')],
        'ordering': ['user_id', 'query', '-created']
    }
