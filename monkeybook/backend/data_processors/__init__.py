
class DataProcessor(object):
    """
    A DataProcessor is responsible for making calls to
    one or more data_connector classes, processing it,
    and returning the processed data for the generator
    to use.

    "Processing it" could mean combining data from multiple
    data "resources", saving it to the database, rejecting
    elements if they don't meet some criteria, and sorting it
    by various values

    """
    data_resource = None
    data_resources = []
    model = None

    def on_all_results(self, *args):
        """
        Any operation that should be performed on all results
        e.g. combining results based on a field, filtering results
        """
        raise NotImplementedError

    def save(self, results):
        """
        Responsible for saving the data
        to the database model
        """
        raise NotImplementedError

    def fetch_results(self):
        # Get the data from the resources
        results = {}
        for resource in self.data_resources:
            results[resource.get_canonical_name()] = resource.run()

        # Run `on_all_results` to perform any shared processing
        results = self.on_all_results(**results)

        # Save to the db if necessary
        if self.model:
            self.save(results)

        # Return the results
        return results


class FacebookDataProcessor(DataProcessor):
    def __init__(self, access_token):
        self.access_token = access_token
        super(FacebookDataProcessor, self).__init__()
