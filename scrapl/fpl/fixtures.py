from scrapl.utils import setup_logger

from .base import FPLScraperBase
from .return_schema import ScraperReturnData, ScraperSubType, ScraperType

logger = setup_logger(__name__)


class FixtureScraper(FPLScraperBase):
    """
    Scrape fixture data from the Fantasy Premier League API.

    Attributes:
        url (str): The URL of the API endpoint for fixtures.

    Methods:
        scrape(): Scrapes the fixture data from the API and returns it.
        parse_fixtures(data): Parses the raw fixture data and returns a filtered list of fixtures.
    """

    url = "https://fantasy.premierleague.com/api/fixtures/"
    scraper_type = "fixtures"

    def __init__(self):
        super().__init__()
        self.fixture_data = None

    def scrape(self):
        """
        Scrapes the fixture data from the Fantasy Premier League API.

        Returns:
            dict: The scraped fixture data.
        """
        d = self.get_response(self.url)
        fixture_data = self.parse_fixtures(d)
        data = ScraperType(
            scraper_type="fixtures", scraper_sub_types={"fixtures": fixture_data}
        )

        self.scraped = True
        self.scraped_data = data
        logger.info("Scraped Fixtures")
        return self.scraped_data

    @staticmethod
    def parse_fixtures(data):
        """
        Parses the raw fixture data and returns a filtered list of fixtures.

        Args:
            data (list): The raw fixture data.

        Returns:
            list: The filtered list of fixtures.
        """
        keepkeys = [
            "event",
            "finished",
            "id",
            "kickoff_time",
            "team_a",
            "team_h",
            "team_a_difficulty",
            "team_h_difficulty",
            "team_a_score",
            "team_h_score",
        ]
        fixture_data = [{key: dict_[key] for key in keepkeys} for dict_ in data]
        return ScraperSubType(
            scraper_sub_type="fixtures", scraper_return_data=fixture_data
        )
