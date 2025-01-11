from scrapl.utils import setup_logger

from .base import FPLScraperBase
from .return_schema import ScraperSubType, ScraperType

logger = setup_logger(__name__)


class PlayerScraper(FPLScraperBase):
    """
    Scrape player data from the Fantasy Premier League API.

    Attributes:
        URL_BASE (str): The base URL for the API endpoint.
        id (int): The ID of the player to scrape.

    Methods:
        scrape(): Scrapes the player data and returns the scraped data.

    """

    URL_BASE = "https://fantasy.premierleague.com/api/element-summary/{ID}/"
    scraper_type = "player"

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.url = self.URL_BASE.format(ID=id)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def scrape(self):
        """
        Scrapes the player data from the API endpoint.

        Returns:
            dict: The scraped player data.

        """
        d = self.get_response(self.url)
        stats = d["history"]
        # self.scraped_data = [ScraperReturnData(data=d["history"])]
        self.scraped_data = ScraperType(
            scraper_type="player",
            scraper_sub_types={
                "player_stats": ScraperSubType(
                    scraper_sub_type="player_stats", scraper_return_data=stats
                )
            },
        )

        self.scraped = True
        # logger.info("Scraped Player info")
        return self.scraped_data
