import datetime
from flask.ext.login import UserMixin
from mongoengine import *


FB_ID_FIELD_LENGTH = 30

class AccessToken(EmbeddedDocument):
    provider = StringField(max_length=255, required=True)
    access_token = StringField(max_length=255, required=True)
    created = DateTimeField(default=lambda: datetime.datetime.utcnow())


class FamilyMember(EmbeddedDocument):
    id = StringField(unique=True, max_length=FB_ID_FIELD_LENGTH, primary_key=True)
    relationship = StringField(max_length=10)


class User(Document, UserMixin):
    id = StringField(unique=True, max_length=FB_ID_FIELD_LENGTH, primary_key=True)
    username = StringField(max_length=255)
    email = EmailField(max_length=255)
    active = BooleanField(default=True)     # TODO: need to check that user is `active`
    access_tokens = SortedListField(EmbeddedDocumentField(AccessToken), ordering='created')

    name = StringField(max_length=255)
    first_name = StringField(max_length=50)
    sex = StringField(max_length=50)
    birthday = DateTimeField()
    affiliations = ListField(DictField())
    age_range = DictField()
    location = DictField()
    locale = StringField(max_length=10)
    pic_square = StringField(max_length=255)
    pic_square_large = StringField(max_length=255)

    relationship_status = StringField(max_length=10)
    significant_other_id = StringField(max_length=FB_ID_FIELD_LENGTH)
    family = ListField(EmbeddedDocumentField(FamilyMember))

    stripe_customer_id = StringField(max_length=255)
    logins = ListField(DateTimeField)

    def __unicode__(self):
        return self.name or ''

    @property
    def friends(self):
        return FacebookFriend.objects(user=self)

    @property
    def access_token_latest(self):
        # Access_tokens is a SortedListField, so we just index it
        return self.access_tokens[-1].access_token

    meta = {
        'indexes': ['id']
    }

    def get_id_str(self):
        return self.username or self.id


class FacebookFriend(Document):
    user = ReferenceField(User)

    uid = StringField(max_length=FB_ID_FIELD_LENGTH, required=True)     # NOT the primary key
    name = StringField(max_length=255, required=True)
    name_uppercase = StringField(max_length=255, required=True)
    first_name = StringField(max_length=50)
    sex = StringField(max_length=10)
    pic_square = StringField(max_length=255)

    meta = {
        'indexes': [('user', 'name_uppercase'), ('book', 'name_uppercase'), ('user', 'uid'), ('book', 'uid')],
        'ordering': ['user', '-top_friends_score']
    }

    def __unicode__(self):
        return self.name


class UserTask(Document):
    """
    An invocation of a Celery taks for a particular user
    basically just an M2M field between User and task_id
    """
    user = ReferenceField(User, required=True)
    task_name = StringField(max_length=255, required=True)
    task_id = StringField(max_length=255, required=True)
    created = DateTimeField(default=lambda: datetime.datetime.utcnow())

    meta = {
        'indexes': ['user', 'task_name'],
        'ordering': ['-created'],
    }

