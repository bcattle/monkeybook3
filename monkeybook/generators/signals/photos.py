from monkeybook.generators.signals import Signal
from monkeybook.data_connnectors.results import ResultField
from monkeybook.data_connnectors.facebook.connectors import friends


class TopPhotoResult(friends.FriendsResult):
    score = ResultField()


class TopPhotosSignal(Signal):
    def __init__(self, *args, **kwargs):
        pass

    def process(self, data):
        pass


class GroupPhotosSignal(Signal):
    def __init__(self, *args, **kwargs):
        pass

    def process(self, data):
        pass


TopPhotosSignal.register()
GroupPhotosSignal.register()
