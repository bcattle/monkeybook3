import re


class DataConnectors(object):
    """
    A container class that holds all `DataConnector` objects
    Stores the result of running them, so they can be re-used
    """
    registry = {}

    def __init__(self):
        self.results = {}

    #@staticmethod
    def run(self, name, *args, **kwargs):
        """
        If the DataProcessor result is in self._results,
        return it. Otherwise re-run the processor
        """
        if name not in self.results:
            resource = DataConnectors.registry[name]()
            self.results[name] = resource.run(*args, **kwargs)

        return self.results[name]


class DataConnector(object):
    @classmethod
    def register(cls):
        DataConnectors.registry[cls.__name__] = cls

    def run(self, *args, **kwargs):
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


# Import and register

from facebook.connectors.friends import FriendsConnector
from facebook.connectors.photos import CommentsOnPhotosOfMeConnector, PhotosOfMeConnector, TaggedWithMeConnector
from facebook.connectors.posts import OthersPostsConnector, OwnerPostsConnector
from facebook.connectors.profile import FamilyConnector, ProfileFieldsConnector, SquareProfilePicConnector

FriendsConnector.register()
CommentsOnPhotosOfMeConnector.register()
PhotosOfMeConnector.register()
TaggedWithMeConnector.register()
OthersPostsConnector.register()
OwnerPostsConnector.register()
FamilyConnector.register()
ProfileFieldsConnector.register()
SquareProfilePicConnector.register()
