from monkeybook.generators.source_data import BookSourceData


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

        photo_tags = self.data_connectors.run('TaggedWithMeConnector',
                                              access_token=self.config.access_token,
                                              end_datetime=self.config.book_end_time)

        comments_on_photos = self.data_connectors.run('CommentsOnPhotosOfMeConnector',
                                                      access_token=self.config.access_token,
                                                      end_datetime=self.config.book_end_time)

        self.photos = self.data_connectors.run('PhotosOfMeConnector',
                                               access_token=self.config.access_token,
                                               end_datetime=self.config.book_end_time)

        # Friends
        self.friends = self.data_connectors.run('FriendsConnector',
                                                access_token=self.config.access_token)

        # Wall posts

        self.wall_posts = self.data_connectors.run('OwnerPostsConnector',
                                                   access_token=self.config.access_token,
                                                   start_datetime=self.config.book_start_time,
                                                   end_datetime=self.config.book_end_time)

        others_posts_from_year = self.data_connectors.run('OthersPostsConnector',
                                                          access_token=self.config.access_token,
                                                          start_datetime=self.config.book_start_time,
                                                          end_datetime=self.config.book_end_time)


        # Add the comments and tags to the photos
        for photo in self.photos:
            photo.tagged_in_photo = photo_tags.get_by_id('object_id', photo.object_id)
            photo.comments = comments_on_photos.get_by_id('object_id', photo.object_id),


        # Combine the two sets of wall posts
        self.wall_posts.merge_no_duplicates('post_id', others_posts_from_year)


        ## Signals

        pass


