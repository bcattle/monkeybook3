from monkeybook.backend.data_processors import FacebookDataProcessor
from monkeybook.data_connnectors.facebook.resources import photos
from monkeybook.data_connnectors.results import ResultField, ResultsCollection


class PhotoResult(photos.PhotosOfMeResult):
    tagged_in_photo = ResultField()
    comments = ResultField()


class PhotoDataProcessor(FacebookDataProcessor):
    data_resources = [
        photos.TaggedWithMeResource,
        photos.PhotosOfMeResource,
        photos.CommentsOnPhotosOfMeResource,
    ]

    def on_all_results(self, tagged_with_me, photos_of_me, comments_on_photos):
        """
        Adds the list of comments and tags to each photo
        """
        processed_results = ResultsCollection()
        for photo in photos_of_me:
            new_photo = PhotoResult(
                base=photo,
                comments=comments_on_photos.get_by_id('object_id', photo.object_id),
                tagged_in_photo=tagged_with_me.get_by_id('object_id', photo.object_id),
            )
            processed_results.append(new_photo)

        # Do we want to do this here?
        # Save the list of photo tags, since we need it for top friends
        self.tagged_with_me = tagged_with_me

        return processed_results

