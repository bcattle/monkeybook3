import calendar
from monkeybook.facebook_connector.results import ResultsCollection
from monkeybook.facebook_connector.tasks import FqlTask


class FqlResource(object):
    fql = None
    result_class = None


    def __init__(self, access_token, storage=None):
        assert self.fql
        assert self.result_class
        self.access_token = access_token
        self.storage = storage


    def run(self, fql=None):
        """
        Runs an FQLTask with the specified query
         - pass through the instance of `storage`
        """
        if fql is None:
            fql = self.fql
        task = FqlTask(fql, self.access_token, self.storage)

        # Get the results
        results = task.get_results()

        # Assign the results to the result class
        results_collection = ResultsCollection()
        for result in results:
            results_collection.append(self.result_class(result))

        return results_collection


    def _convert_datetime_to_timestamp(self, dt):
        return calendar.timegm(dt.utctimetuple())
