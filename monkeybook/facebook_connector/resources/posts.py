from monkeybook.facebook_connector.resources import FqlResource
from monkeybook.facebook_connector.results import ResourceResult, ResultField, IntegerField, TimestampField


class PostsResult(ResourceResult):
    post_id = IntegerField()
    actor_id = IntegerField()
    created_time = TimestampField()
    comments = ResultField()
    likes  = ResultField()
    message = ResultField()


class OwnerPostsFromYearTask(FqlResource):
    fql = '''
        SELECT post_id, actor_id, created_time, comments, likes, message FROM stream
            WHERE source_id=me() AND message!='' AND filter_key='owner'
            %s LIMIT 500
    '''
    result_class = PostsResult

    def run(self, start_datetime=None, end_datetime=None):
        # If start/end specified, append to `fql`
        extra_fql = ''
        if start_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(start_datetime)
            extra_fql += ' AND created > %s' % unix_end_time
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            extra_fql += ' AND created < %s' % unix_end_time
        self.fql %= extra_fql

        super(OwnerPostsFromYearTask, self).run()

    # Set default values for comments.count and likes.count


class OthersPostsFromYearTask(OwnerPostsFromYearTask):
    fql = '''
        SELECT post_id, actor_id, created_time, comments, likes, message FROM stream
            WHERE source_id=me() AND message!='' AND filter_key='others'
            %s LIMIT 500
    '''
