import re
from facebook import GraphAPI


class BaseTask(object):
    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = self._get_canonical_name(self.__class__.__name__)

    def _get_canonical_name(self, string):
        return re.sub(r'([A-Z])([A-Z])', r'\1_\2',
                      re.sub(r'([a-zA-Z])([A-Z])', r'\1_\2', string)).lower()[:-5]


class FqlTask(BaseTask):
    """
    Encapsulates a single FQL query
    The optional `storage` and `cache` classes allow the contents
    of a FQL call to be stored and retrieved in lieu of re-running the query
    """
    def __init__(self, fql, access_token, storage=None, prefer_cache=False, store_results=True, override_name=None):
        self.fql = merge_spaces(fql)
        self.storage = storage
        self.prefer_cache = prefer_cache
        self.store_results = store_results
        self.graph_api = GraphAPI(access_token)

        super(FqlTask, self).__init__(override_name)


    def get_results(self):
        if self.prefer_cache:
            # Check the cache for the query
            cache_result = self.storage.retrieve(self.fql)
            if cache_result:
                return cache_result

        fql_results = self.graph_api.fql(self.fql)

        # TODO: if there was an error, look in the cache as a fallback
        if self.store_results and self.storage:
            # Store the results, using the storage class
            self.storage.store(
                query_type=self.name,
                query=self.fql,
                results=fql_results,
            )
        return fql_results


def merge_spaces(s):
    """
    Combines consecutive spaces into one,
    useful for cleaning up multiline strings
    """
    return " ".join(s.split())
