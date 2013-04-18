from monkeybook.facebook_connector.results import ResultsCollection
from monkeybook.facebook_connector.tasks import FqlTask


class FqlResource(object):
    def __init__(self, access_token, storage=None):
        assert self.fql
        assert self.result_class
        self.access_token = access_token
        self.storage = storage

    def run(self):
        """
        Runs an FQLTask with the specified query
        pass thorugh the instance of `storage`
        """
        task = FqlTask(self.fql, self.access_token, self.storage)

        # Get the results
        results = task.get_results()

        # Assign the results to the result class
        results_collection = ResultsCollection()
        for result in results:
            results_collection.append(self.result_class(result))

        return results_collection


