"""
scraper.py

This module contains classes and methods for scraping data from the Fantasy Premier League (FPL) API.
It includes a base scraper class with common functionality and a specific scraper for general information.

Classes:
    FPLScraperBase: An abstract base class for FPL scrapers.
    GenInfoScraper: A concrete implementation of FPLScraperBase for scraping general information.
    FixtureScraper: A concrete implementation of FPLScraperBase for scraping fixture data.
    GameweekScraper: A concrete implementation of FPLScraperBase for scraping high-level player stats for all gameweeks.
    PlayerScraper: A concrete implementation of FPLScraperBase for scraping granular data for a specific player.

Dependencies:
    - requests: For making HTTP requests.
    - pandas: For data manipulation and analysis.
    - json: For handling JSON data.
    - datetime: For handling date and time operations.
    - abc: For defining abstract base classes.
    - tenacity: For retrying operations with customizable behavior.
    - lionel.utils: For setting up logging.

Usage:
    Create an instance of a scraper class and call its `scrape` method to retrieve data from the FPL API.
"""

import requests
import pandas as pd
import json
import datetime as dt
from abc import ABC, abstractmethod
from tenacity import retry, stop_after_attempt, wait_fixed

from scrapl.utils import setup_logger

logger = setup_logger(__name__)


class FPLScraperBase(ABC):
    """
    Abstract base class for Fantasy Premier League (FPL) scrapers.
    """

    def __init__(self):
        self.response_data = None
        self.scraped_data = {}
        self.scraped = False

    @property
    @abstractmethod
    def url(self):
        """
        The URL to scrape data from.
        """
        pass

    @abstractmethod
    def scrape(self) -> dict:
        """
        Scrapes data from the specified URL and returns the scraped data as a dictionary.

        Returns:
            dict: The scraped data.
        """
        pass

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5), reraise=True)
    def get_response(self, url: str):
        """
        Sends a GET request to the specified URL and returns the response.

        Args:
            url (str): The URL to send the request to.

        Returns:
            Response: The response object.

        Raises:
            AssertionError: If the response status code is not OK (200).
        """
        r = requests.get(url)
        assert r.ok
        d = r.json()
        self.response_data = d
        return d

    def to_json(self, fname):
        """
        Converts the scraped data to JSON format.
        """
        json.dump(self.scraped_data, fname, "w")


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
        self.scraped_data["team_map"] = self.get_team_map(d)
        self.scraped_data["gw_deadlines"] = self.get_gw_deadlines(d)
        self.scraped_data["element_map"] = self.get_element_name_map(d)
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
        return team_map

    @staticmethod
    def get_gw_deadlines(response_data):
        """
        Retrieves the gameweek deadlines from the response data.

        Returns:
            dict: A dictionary mapping gameweek IDs to deadline times.
        """
        gw_deadlines = {gw["id"]: gw["deadline_time"] for gw in response_data["events"]}
        # self.gw_deadlines = gw_deadlines
        return gw_deadlines

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
        # self.element_map = element_name_map
        return element_name_map


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
        self.scraped = True
        self.scraped_data["fixtures"] = fixture_data
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
        return fixture_data


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
        self.scraped_data[f"gw_stats_{self.gameweek}"] = stats
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
        self.scraped_data[f"player_stats_{self.id}"] = stats
        # logger.info("Scraped Player info")
        return self.scraped_data
