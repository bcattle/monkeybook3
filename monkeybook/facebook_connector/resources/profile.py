from monkeybook.facebook_connector.resources import FqlResource
from monkeybook.facebook_connector.results import ResourceResult, ResultField


class ProfileFieldsResult(ResourceResult):
    uid = ResultField(required=True)
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
    significant_other_id = ResultField()


class ProfileFieldsResource(FqlResource):
    fql = '''
        SELECT uid, username, email, name, affiliations, age_range, current_location,
            first_name, pic_square, locale, relationship_status, sex,
            significant_other_id
            FROM user WHERE uid = me()
    '''
    result_class = ProfileFieldsResult



# class FamilyTask(FQLTask):
#     fql = '''
#         SELECT uid, relationship FROM family WHERE profile_id = me()
#     '''
#
#     def on_results(self, results):
#         return results
#
#     def save(self, results):
#         # Overwrites the existing list
#         self.user.family = [FamilyMember(id=str(f['uid']), relationship=f['relationship'])
#                             for f in results]
#         self.user.save()
#
#
# class SquareProfilePicTask(FQLTask):
#     fql = '''
#         SELECT url,real_size FROM square_profile_pic WHERE id = me() AND size = 160
#     '''
#
#     def on_results(self, results):
#         return results[0]
#
#     def save(self, results):
#         self.user.pic_square_large = results['url']
#         self.user.save()
#
