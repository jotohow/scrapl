from scrapl.utils import setup_logger

from .base import FPLScraperBase
from .return_schema import ScraperReturnData, ScraperSubType, ScraperType

logger = setup_logger(__name__)


class GenInfoScraper(FPLScraperBase):
    """
    Scraper for general information from the Fantasy Premier League API.

    Attributes:
        url (str): The URL of the API endpoint.
        team_map (dict): A dictionary mapping team IDs to team information.
        gw_deadlines (dict): A dictionary mapping gameweek IDs to deadline times.
        element_map (dict): A dictionary mapping element IDs to element information.
    """

    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    scraper_type = "general"

    def __init__(self):
        super().__init__()
        self.gw_deadlines = None

    def scrape(self):
        """
        Scrapes the general information from the API endpoint.

        Returns:
            dict: A dictionary containing the scraped data.
        """
        d = self.get_response(self.url)

        scraped_data = ScraperType(
            scraper_type="general",
            scraper_sub_types={
                "team_map": self.get_team_map(d),
                "gw_deadlines": self.get_gw_deadlines(d),
                "element_map": self.get_element_name_map(d),
            },
        )
        self.scraped_data = scraped_data
        self.scraped = True
        logger.info("Scraped general info")
        return self.scraped_data

    @staticmethod
    def get_team_map(response_data):
        """
        Retrieves the team map from the response data.

        Returns:
            dict: A dictionary mapping team IDs to team information.
        """
        team_map = {
            team["id"]: {
                "name": team["name"],
                "strength": team["strength"],
                "strength_overall_home": team["strength_overall_home"],
                "strength_overall_away": team["strength_overall_away"],
                "strength_attack_home": team["strength_attack_home"],
                "strength_attack_away": team["strength_attack_away"],
                "strength_defence_home": team["strength_defence_home"],
                "strength_defence_away": team["strength_defence_away"],
            }
            for team in response_data["teams"]
        }
        return_data = ScraperSubType(
            scraper_sub_type="team_map",
            scraper_return_data=[team_map],
        )
        return return_data

    @staticmethod
    def get_gw_deadlines(response_data):
        """
        Retrieves the gameweek deadlines from the response data.

        Returns:
            dict: A dictionary mapping gameweek IDs to deadline times.
        """
        gw_deadlines = {gw["id"]: gw["deadline_time"] for gw in response_data["events"]}
        return_data = ScraperSubType(
            scraper_sub_type="gw_deadlines",
            scraper_return_data=[gw_deadlines],
        )
        return return_data

    @staticmethod
    def get_element_name_map(response_data):
        """
        Retrieves the element name map from the response data.

        Returns:
            dict: A dictionary mapping element IDs to element information.
        """
        el = response_data["elements"]
        element_name_map = {
            el[i]["id"]: {
                "id": el[i]["id"],
                "web_name": el[i]["web_name"],
                "first_name": el[i]["first_name"],
                "second_name": el[i]["second_name"],
                "team_id": el[i]["team"],
                "element_type": el[i]["element_type"],
            }
            for i in range(len(el))
        }
        return_data = ScraperSubType(
            scraper_sub_type="element_map", scraper_return_data=[element_name_map]
        )
        return return_data
