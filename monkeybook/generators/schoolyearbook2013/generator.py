from monkeybook.generators.generate_book import BookGenerator
from monkeybook.generators.schoolyearbook2013.config import BookGeneratorConfig


class SchoolYearbook2013Generator(BookGenerator):
    config = BookGeneratorConfig()
    source_data = SchoolYearbook2013SourceData()
