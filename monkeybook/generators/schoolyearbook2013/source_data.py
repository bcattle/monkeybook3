from monkeybook.generators.source_data import BookSourceData


class SchoolYearbook2013SourceData(BookSourceData):
    def __init__(self, config):
        super(SchoolYearbook2013SourceData, self).__init__(config)

        self.friends = []            # FriendsResource
        self.photos = []             # PhotoDataProcessor
        self.wall_posts = []         # WallPostDataProcessor


    def collect_data(self):
        ## Run all of the data connectors we need
        # These need to run in parallel
        tagged_with_me = tags_resource.run(access_token, end_datetime)
        photos_of_me = photos_resource.run(access_token, end_datetime)
        comments_on_photos = comments_resource.run(access_token, end_datetime)

        # Top friends
        self.friends = self.data_connectors.run('FriendsResource',
                                                access_token=self.config.access_token)

        import ipdb
        ipdb.set_trace()

        # Photos
        self.photos = self.data_processors.fetch_results('PhotoDataProcessor',
                                                         access_token=self.config.access_token,
                                                         end_datetime=self.config.book_end_time)

        # Wall posts
        self.wall_posts = self.data_processors.fetch_results('WallPostDataProcessor',
                                                             access_token=self.config.access_token,
                                                             end_datetime=self.config.book_end_time)

        # Add the list of comments and tags to each photo
        processed_results = ResultsCollection()
        for photo in photos_of_me:
            new_photo = PhotoResult(
                base=photo,
                comments=comments_on_photos.get_by_id('object_id', photo.object_id),
                tagged_in_photo=tagged_with_me.get_by_id('object_id', photo.object_id),
            )
            processed_results.append(new_photo)


        # Combine the two sets of wall posts
        owner_posts_from_year = owner_posts_resource.run(access_token=self.access_token,
                                                         start_datetime=start_datetime,
                                                         end_datetime=end_datetime)
        others_posts_from_year = others_posts_resource.run(access_token=self.access_token,
                                                           start_datetime=start_datetime,
                                                           end_datetime=end_datetime)

        processed_results = copy.copy(owner_posts_from_year)
        processed_results.merge_no_duplicates(self, 'post_id', others_posts_from_year)

        ## Signals

        pass


