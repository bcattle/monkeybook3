import calendar
from monkeybook.data_connnectors import DataConnector
from monkeybook.data_connnectors.results import ResultsCollection, BlankFieldError
from monkeybook.data_connnectors.facebook.tasks import FqlTask


class FqlConnector(DataConnector):
    def __init__(self):
        assert self.result_class, 'An FqlConnector must specify a result class'

    def run(self, access_token, storage=None, fql=None):
        """
        Runs an FQLTask with the specified query
         - pass through the instance of `storage`
        """
        if fql is None:
            fql = self.fql
        task = FqlTask(fql, access_token, storage)

        # Get the results
        results = task.get_results()

        # Assign the results to the result class
        results_collection = ResultsCollection()
        for result in results:
            try:
                results_collection.append(self.result_class(result))
            except BlankFieldError:
                import ipdb
                ipdb.set_trace()

                pass

        return results_collection

    def _convert_datetime_to_timestamp(self, dt):
        return calendar.timegm(dt.utctimetuple())
