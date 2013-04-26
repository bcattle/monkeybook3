from monkeybook.data_connnectors.facebook.connectors import FqlConnector
from monkeybook.data_connnectors.results import ConnectorResult, ResultField, IntegerField


class ProfileFieldsResult(ConnectorResult):
    uid = IntegerField(required=True)
    username = ResultField(required=True)
    email = ResultField()
    locale = ResultField()
    name = ResultField()
    first_name = ResultField()
    age_range = ResultField()
    current_location = ResultField()
    affiliations = ResultField()
    pic_square = ResultField()
    relationship_status = ResultField()
    sex = ResultField()
    significant_other_id = IntegerField()
    @property
    def id(self):
      return self.uid


class ProfileFieldsConnector(FqlConnector):
    fql = '''
        SELECT uid, username, email, name, affiliations, age_range, current_location,
            first_name, pic_square, locale, relationship_status, sex,
            significant_other_id
            FROM user WHERE uid = me()
    '''
    result_class = ProfileFieldsResult


class FamilyResult(ConnectorResult):
    uid = IntegerField()
    relationship = ResultField()


class FamilyConnector(FqlConnector):
    fql = '''
        SELECT uid, relationship FROM family WHERE profile_id = me()
    '''
    result_class = FamilyResult


class SquareProfilePicResult(ConnectorResult):
    url = ResultField()
    real_size = ResultField()


class SquareProfilePicConnector(FqlConnector):
    fql = '''
        SELECT url,real_size FROM square_profile_pic WHERE id = me() AND size = 160
    '''
    result_class = SquareProfilePicResult
