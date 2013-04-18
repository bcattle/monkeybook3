from monkeybook.facebook_connector.resources import FqlResource
from monkeybook.facebook_connector.results import ResourceResult, ResultField, IntegerField, TimestampField


class PhotosOfMeResult(ResourceResult):
    object_id = IntegerField()
    images = ResultField()
    created = TimestampField()
    comment_info = ResultField()
    like_info = ResultField()
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
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            self.fql %= 'AND created < %s ' % unix_end_time
        else:
            self.fql %= ''

        super(PhotosOfMeTask, self).run()

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

        super(CommentsOnPhotosOfMeResource, self).run()
