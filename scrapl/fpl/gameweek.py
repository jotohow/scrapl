from scrapl.utils import setup_logger

from .base import FPLScraperBase
from .return_schema import ScraperSubType, ScraperType

logger = setup_logger(__name__)


class GameweekScraper(FPLScraperBase):
    """
    Scraper for gameweek stats from the Fantasy Premier League API.

    Attributes:
        URL_BASE (str): The base URL for the API endpoint.
        gameweek (int): The gameweek number.
        url (str): The complete URL for the API endpoint.
        scraped_data (dict): A dictionary to store the scraped data.
        scraped (bool): A flag indicating whether the data has been scraped or not.
    """

    URL_BASE = "https://fantasy.premierleague.com/api/event/{GW}/live/"

    scraper_type = "gameweek"

    def __init__(self, gameweek):
        """
        Initializes a new instance of the GameweekScraper class.

        Args:
            gameweek (int): The gameweek number.
        """
        super().__init__()
        self.gameweek = gameweek
        self.url = self.URL_BASE.format(GW=gameweek)
        self.scraped_data = {}
        self.scraped = False

    @property
    def url(self):
        """
        The complete URL for the API endpoint.

        Returns:
            str: The URL.
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the URL for the API endpoint.

        Args:
            url (str): The URL.
        """
        self._url = url

    def scrape(self):
        """
        Scrapes the gameweek stats from the API.

        Returns:
            dict: The scraped data.
        """
        d = self.get_response(self.url)
        stats = self.parse_gameweek_stats(d)
        data = ScraperType(
            scraper_type="gameweek",
            scraper_sub_types={
                "gw_stats": ScraperSubType(
                    scraper_sub_type="gw_stats",
                    scraper_return_data=stats,
                )
            },
        )
        self.scraped_data = data
        self.scraped = True
        return self.scraped_data

    @staticmethod
    def parse_gameweek_stats(response_data):
        """
        Parses the gameweek stats from the API response.

        Returns:
            list: A list of dictionaries containing the stats for each player.
        """
        stats = []
        for player in response_data["elements"]:
            d_ = {"id": player["id"]}
            d_.update(player["stats"])
            d_.update({"fixture_id": player["explain"][0]["fixture"]})
            stats.append(d_)
        return stats
