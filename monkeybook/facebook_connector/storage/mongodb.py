import datetime
from mongoengine import *

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
