from monkeybook.facebook_connector.resources import FqlResource
from monkeybook.facebook_connector.results import ResourceResult, ResultField, IntegerField, TimestampField


class TaggedWithMeResult(ResourceResult):
    subject = IntegerField()       # sometimes comes back empty
    object_id = IntegerField(required=True)
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
    result_class = TaggedWithMeResult

    def run(self, end_datetime=None):
        # If end_datetime is specified, append to `fql`
        fql = self.fql
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            fql %= 'AND created < %s ' % unix_end_time
        else:
            fql %= ''

        return super(TaggedWithMeResource, self).run(fql)

        # specify a default value for `created`
        # throw away tags with no `photo_id`?


class PhotosOfMeResult(ResourceResult):
    object_id = IntegerField()
    images = ResultField()      # contains list('height', 'source', 'width', 'height')
    created = TimestampField()
    comment_info = ResultField()    # contains 'can_comment', 'comment_count', 'comment_order'
    like_info = ResultField()       # contains 'can_like', 'like_count', u'user_likes'
    album_object_id = IntegerField()
    caption = ResultField()


class PhotosOfMeTask(FqlResource):
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

    def run(self, end_datetime=None):
        # If end_datetime is specified, append to `fql`
        fql = self.fql
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            fql %= 'AND created < %s ' % unix_end_time
        else:
            fql %= ''

        return super(PhotosOfMeTask, self).run(fql)

    # Run process_photo_results


class CommentsOnPhotosOfMeResult(ResourceResult):
    object_id = IntegerField()
    fromid = IntegerField()
    time = TimestampField()
    text = ResultField()
    likes = IntegerField()
    user_likes = ResultField()


class CommentsOnPhotosOfMeResource(FqlResource):
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

    def run(self, end_datetime=None):
        # If end_datetime is specified, append to `fql`
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            self.fql %= 'AND time < %s ' % unix_end_time
        else:
            self.fql %= ''

        return super(CommentsOnPhotosOfMeResource, self).run()
