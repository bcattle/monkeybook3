from monkeybook.generators.signals import Signal
from monkeybook.data_connnectors.results import ResultField
from monkeybook.data_connnectors.facebook.connectors import friends


class TopPostsResult(friends.FriendsResult):
    score = ResultField()


class TopPostsSignal(Signal):
    def __init__(self, *args, **kwargs):
        pass

    def process(self, data):
        pass


class BirthdayPostsSignal(Signal):
    def __init__(self, *args, **kwargs):
        pass

    def process(self, data):
        pass


TopPostsSignal.register()
BirthdayPostsSignal.register()
