from monkeybook.generators.signals import Signal
from monkeybook.data_connnectors.results import ResultField
from monkeybook.data_connnectors.facebook.connectors import friends


class TopFriendsResult(friends.FriendsResult):
    photo_tags = ResultField()


class TopFriendsSignal(Signal):
    def process(self, data):
        """
        This receives a
        """
        # Data contains
        #
        pass

TopFriendsSignal.register()
