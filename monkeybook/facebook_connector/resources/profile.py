from monkeybook.facebook_connector.resources import FqlResource
from monkeybook.facebook_connector.results import ResourceResult, ResultField, IntegerField


class ProfileFieldsResult(ResourceResult):
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


class ProfileFieldsResource(FqlResource):
    fql = '''
        SELECT uid, username, email, name, affiliations, age_range, current_location,
            first_name, pic_square, locale, relationship_status, sex,
            significant_other_id
            FROM user WHERE uid = me()
    '''
    result_class = ProfileFieldsResult


class FamilyResult(ResourceResult):
    uid = IntegerField()
    relationship = ResultField()


class FamilyResource(FqlResource):
    fql = '''
        SELECT uid, relationship FROM family WHERE profile_id = me()
    '''
    result_class = FamilyResult


class SquareProfilePicResult(ResourceResult):
    url = ResultField()
    real_size = ResultField()


class SquareProfilePicResource(FqlResource):
    fql = '''
        SELECT url,real_size FROM square_profile_pic WHERE id = me() AND size = 160
    '''
