from monkeybook.facebook_connector.resources import FqlResource
from monkeybook.facebook_connector.results import ResourceResult, ResultField, IntegerField, TimestampField


class FriendsResult(ResourceResult):
    uid = IntegerField(required=True)
    name = ResultField(required=True)
    first_name = ResultField()
    pic_square = ResultField(required=True)
    sex = ResultField()


class FriendsResource(FqlResource):
    """
    Pulls all of the user's friends
    """
    fql = '''
        SELECT uid, first_name, name, pic_square, sex FROM user
            WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())
    '''
    result_class = FriendsResult
    # Need to add the field 'name_uppercase'


class TagWithMeResult(ResourceResult):
    subject = IntegerField(required=True)
    photo_id = IntegerField(required=True)
    created = TimestampField()     # 2/20: sometimes the `created` field comes back None


class TaggedWithMeResource(FqlResource):
    """
    Returns all of the tags of all photos I am in
    We do this because we can't pull `tags` from `photo` table.
    --> This is a workaround for the fact that
        facebook WHERE queries are broken for `photo_tags`
    """
    fql = '''
        SELECT subject, object_id, created FROM photo_tag WHERE object_id IN
            (SELECT object_id FROM photo_tag WHERE subject=me())
        AND subject!=me() %s ORDER BY created DESC
    '''

    def run(self, end_datetime=None):
        # If end_datetime is specified, append to `fql`
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            self.fql %= 'AND created < %s ' % unix_end_time
        else:
            self.fql %= ''

        super(TaggedWithMeResource, self).run()

    # specify a default value for `created`
