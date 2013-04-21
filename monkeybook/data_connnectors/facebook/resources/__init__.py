import calendar, re
from monkeybook.data_connnectors.results import ResultsCollection
from monkeybook.data_connnectors.facebook.tasks import FqlTask


class ConnectorResource(object):
    def run(self):
        """
        Runs the resource,
        retrieving data from the server
        """
        raise NotImplementedError

    def get_canonical_name(self):
        """
        Returns a nice name for CamelCased classes
        e.g. `ConnectorResource` returns 'connector_resource'
        """
        string = self.__class__.__name__
        return re.sub(r'([A-Z])([A-Z])', r'\1_\2',
                      re.sub(r'([a-zA-Z])([A-Z])', r'\1_\2', string)).lower()[:-5]


class FqlResource(ConnectorResource):
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
