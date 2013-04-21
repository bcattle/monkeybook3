from monkeybook.data_connnectors.facebook.resources import FqlResource
from monkeybook.data_connnectors.results import ResourceResult, ResultField, IntegerField, TimestampField


class PostsResult(ResourceResult):
    post_id = ResultField()
    actor_id = IntegerField()
    created_time = TimestampField()
    comments = ResultField()        # contains 'can_post', 'can_remove', 'comment_list', 'count'
    likes  = ResultField()          # contains 'can_like', 'count', 'friends', 'href', u'sample', 'user_likes'
    message = ResultField()
    # Probably want other fields here


## Note: these can take a LONG time to run (~20 secs) if
## not limited by time or count

class OwnerPostsFromYearTask(FqlResource):
    fql = '''
        SELECT post_id, actor_id, created_time, comments, likes, message FROM stream
            WHERE source_id=me() AND message!='' AND filter_key='owner' %s
    '''
    result_class = PostsResult

    def run(self, start_datetime=None, end_datetime=None, limit=500):
        # If start/end specified, append to `fql`
        extra_fql = ''
        if start_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(start_datetime)
            extra_fql += ' AND created > %s' % unix_end_time
        if end_datetime:
            unix_end_time = self._convert_datetime_to_timestamp(end_datetime)
            extra_fql += ' AND created < %s' % unix_end_time

        fql = self.fql % (extra_fql + ' LIMIT %d' % limit)
        return super(OwnerPostsFromYearTask, self).run(fql)

    # Set default values for comments.count and likes.count


class OthersPostsFromYearTask(OwnerPostsFromYearTask):
    fql = '''
        SELECT post_id, actor_id, created_time, comments, likes, message FROM stream
            WHERE source_id=me() AND message!='' AND filter_key='others' %s
    '''
