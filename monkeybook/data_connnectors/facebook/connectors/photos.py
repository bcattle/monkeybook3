from monkeybook.data_connnectors.facebook.connectors import FqlConnector
from monkeybook.data_connnectors.results import ConnectorResult, ResultField, IntegerField, TimestampField


class TaggedWithMeResult(ConnectorResult):
    object_id = IntegerField(required=True)
    subject = IntegerField()       # sometimes comes back empty
    created = TimestampField()     # 2/20: sometimes the `created` field comes back None


class TaggedWithMeConnector(FqlConnector):
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
    result_class = TaggedWithMeResult

    def run(self, access_token, storage=None, end_datetime=None):
        # If end_datetime is specified, append to `fql`
        fql = self.fql
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            fql %= 'AND created < %s ' % unix_end_time
        else:
            fql %= ''

        return super(TaggedWithMeConnector, self).run(access_token, storage, fql)

        # specify a default value for `created`
        # throw away tags with no `photo_id`?


class PhotosOfMeResult(ConnectorResult):
    object_id = IntegerField()
    images = ResultField()      # contains list('height', 'source', 'width', 'height')
    created = TimestampField()
    comment_info = ResultField()    # contains 'can_comment', 'comment_count', 'comment_order'
    like_info = ResultField()       # contains 'can_like', 'like_count', u'user_likes'
    album_object_id = IntegerField()
    caption = ResultField()
    # These are added in the `source_data` class
    comments = ResultField()
    people_tagged = ResultField()


class PhotosOfMeConnector(FqlConnector):
    """
    Returns all of the photos the current user is tagged in.
    """
    fql = '''
        SELECT object_id, images, created, comment_info, like_info,
            album_object_id, caption FROM photo
            WHERE object_id IN
                (SELECT object_id FROM photo_tag WHERE subject=me())
            %s
    '''
    result_class = PhotosOfMeResult

    def run(self, access_token, storage=None, end_datetime=None):
        # If end_datetime is specified, append to `fql`
        fql = self.fql
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            fql %= 'AND created < %s ' % unix_end_time
        else:
            fql %= ''

        return super(PhotosOfMeConnector, self).run(access_token, storage, fql)

    # Run process_photo_results


class CommentsOnPhotosOfMeResult(ConnectorResult):
    object_id = IntegerField()
    fromid = IntegerField()
    time = TimestampField()
    text = ResultField()
    likes = IntegerField()
    user_likes = ResultField()


class CommentsOnPhotosOfMeConnector(FqlConnector):
    """
    Returns all comments on the photos the current user is tagged in
    """
    fql = '''
        SELECT object_id, fromid, time, text, likes, user_likes
            FROM comment WHERE object_id IN
                (SELECT object_id FROM photo_tag WHERE subject=me())
            %s
    '''
    result_class = CommentsOnPhotosOfMeResult

    def run(self, access_token, storage=None, end_datetime=None):
        # If end_datetime is specified, append to `fql`
        fql = self.fql
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            fql %= 'AND time < %s ' % unix_end_time
        else:
            fql %= ''

        return super(CommentsOnPhotosOfMeConnector, self).run(access_token, storage, fql)
