import copy
from monkeybook.backend.data_processors import FacebookDataProcessor
from monkeybook.data_connnectors.facebook.resources import posts


class PostsDataProcessor(FacebookDataProcessor):
    data_resources = [
        posts.OwnerPostsResource,
        posts.OthersPostsResource,
    ]

    def on_all_results(self, owner_posts_from_year, others_posts_from_year):
        """
        Combines the two lists of photos
        """
        processed_results = copy.copy(owner_posts_from_year)
        processed_results.merge_no_duplicates(self, 'post_id', others_posts_from_year)
        return processed_results


# Strip posts that have an attachment that is a photo?
#    .filter(lambda x: 'attachment' in x and 'fb_object_type' in x['attachment'] and x['attachment'])