from monkeybook.data_connnectors.facebook.connectors import FqlConnector
from monkeybook.data_connnectors.results import ConnectorResult, ResultField, IntegerField


class FriendsResult(ConnectorResult):
    uid = IntegerField(required=True)
    name = ResultField(required=True)
    first_name = ResultField()
    pic_square = ResultField(required=True)
    sex = ResultField()
    
    @property
    def id(self):
      return self.uid


class FriendsConnector(FqlConnector):
    """
    Pulls all of the user's friends
    """
    fql = '''
        SELECT uid, first_name, name, pic_square, sex FROM user
            WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())
    '''
    result_class = FriendsResult
    # Need to add the field 'name_uppercase'

