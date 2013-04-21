from monkeybook.data_connnectors.facebook.resources import FqlResource
from monkeybook.data_connnectors.results import ResourceResult, ResultField, IntegerField


class FriendsResult(ResourceResult):
    uid = IntegerField(required=True)
    name = ResultField(required=True)
    first_name = ResultField()
    pic_square = ResultField(required=True)
    sex = ResultField()


class FriendsResource(FqlResource):
    """
    Pulls all of the user's friends
    """
    fql = '''
        SELECT uid, first_name, name, pic_square, sex FROM user
            WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())
    '''
    result_class = FriendsResult
    # Need to add the field 'name_uppercase'

