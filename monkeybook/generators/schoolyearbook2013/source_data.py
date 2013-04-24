from monkeybook.generators.source_data import BookSourceData
from concurrent import futures

class SchoolYearbook2013SourceData(BookSourceData):
    def __init__(self, config):
        super(SchoolYearbook2013SourceData, self).__init__(config)

        self.friends = []
        self.photos = []
        self.wall_posts = []


    def collect_data(self):
        ## Run all of the data connectors needed for the book
        # These need to run in parallel

        # Photos
        results = {}
        executor = futures.ThreadPoolExecutor(max_workers=10)
        for var in ('TaggedWithMeConnector', 
                    'CommentsOnPhotosOfMeConnector',
                    'PhotosOfMeConnector'):
          results[var] = executor.submit(self.data_connectors.run, var,
                                         access_token=self.config.access_token,
                                         end_datetime=self.config.book_end_time)
                                         
        results['FriendsConnector'] = executor.submit(self.data_connectors.run, 
                                                      'FriendsConnector',
                                                      access_token=self.config.access_token)
        
        for var in ('OwnerPostsConnector', 
                    'OthersPostsConnector'):
          results[var] = executor.submit(self.data_connectors.run, var,
                                         access_token=self.config.access_token,
                                         start_datetime=self.config.book_start_time,
                                         end_datetime=self.config.book_end_time)

                                                      
        # Get all the results.
        self.friends = results['FriendsConnector'].result()
        self.wall_posts = results['OwnerPostsConnector'].result()
        self.friends = results['PhotosOfMeConnector'].result()
        photo_tags = results['TaggedWithMeConnector'].result()
        comment_on_photos = results['CommentsOnPhotosOfMeConnector'].result()
        others_posts_from_year = results['OthersPostsConnector'].result()
        
        # Add the comments and tags to the photos
        for photo in self.photos:
            photo.tagged_in_photo = photo_tags.get_by_field('object_id', photo.object_id)
            photo.comments = comments_on_photos.get_by_field('object_id', photo.object_id),


        # Combine the two sets of wall posts
        self.wall_posts.merge_no_duplicates('post_id', others_posts_from_year)


        ## Signals

        pass


