"""
scraper.py

This module defines the BetScraper class, an abstract base class for scraping betting odds data from the Odds API,
and its two child classes, FutureBetScraper and HistoricalBetScraper, which implement specific scraping endpoints.
It includes methods for retrieving and processing game data, and provides a structure for future and historical scrapes.

Classes:
    BetScraper: An abstract base class for scraping betting odds data.
    FutureBetScraper: A class for scraping future betting odds data.
    HistoricalBetScraper: A class for scraping historical betting odds data.

Dependencies:
    - numpy: For numerical operations.
    - datetime: For handling date and time operations.
    - pandas: For data manipulation and analysis.
    - os: For interacting with the operating system.
    - requests: For making HTTP requests.
    - dotenv: For loading environment variables from a .env file.
    - abc: For defining abstract base classes.
    - scrape.bet.game: For the Game class used to represent game data.

Usage:
    Create an instance of FutureBetScraper or HistoricalBetScraper to scrape future or historical betting odds data.
"""

import numpy as np
import datetime as dt
import pandas as pd
import os
import requests
from dotenv import dotenv_values
from abc import ABCMeta, abstractmethod

from scrape.bet.game import Game


ENV_VARS = dotenv_values()


class BetScraper(metaclass=ABCMeta):
    """
    Abstract base class for bet scrapers.
    """

    BASE_URL = "https://api.the-odds-api.com//v4/sports/"
    SPORT = "soccer_epl"
    REGIONS = "uk"
    MARKETS = "h2h"
    API_KEY = os.environ.get("API_KEY") or ENV_VARS["API_KEY"]
    NAME_MAP = {
        "Manchester United": "Manchester Utd",
        "Tottenham Hotspur": "Tottenham",
        "Nottingham Forest": "Nottingham",
        "Brighton and Hove Albion": "Brighton",
        "Leicester City": "Leicester",
        "Leeds United": "Leeds",
        "Newcastle United": "Newcastle",
        "West Ham United": "West Ham",
        "Wolverhampton Wanderers": "Wolves",
        "Sheffield United": "Sheffield Utd",
    }

    def __init__(self):
        """
        Initializes an instance of BetScraper.
        """
        self.games = []

    @property
    @abstractmethod
    def odds_endpoint(self):
        """
        Abstract property to be defined for each of future
        and historical scrapes.
        """
        pass

    def _get_response(self, url) -> list:
        """
        Sends a GET request to the specified URL and returns the response.

        Args:
            url (str): The URL to send the request to.

        Returns:
            list: The response from the request.
        """
        r = requests.get(url)
        assert r.ok
        return r

    def run_scrape(self):
        """
        Runs the scrape by sending a request to the odds endpoint,
        creating Game objects from the response, and adding them to
        the list of games.

        Returns:
            list: The list of Game objects scraped.
        """
        response = self._get_response(self.odds_endpoint)
        response_dict = response.json()
        games = [Game(game_dict) for game_dict in response_dict]
        self.games.extend(games)
        return games

    def to_df(self):
        """
        Converts the list of games to a pandas DataFrame.

        Returns:
            pandas.DataFrame: The DataFrame containing the game data.

        Raises:
            Exception: If the scrape has not been run yet.
        """
        if len(self.games) == 0:
            raise Exception("Run the scrape first")
        else:
            df = pd.DataFrame.from_dict([game.to_dict() for game in self.games])
            df = df.replace(
                {"home_team": BetScraper.NAME_MAP, "away_team": BetScraper.NAME_MAP}
            )
            df = df.rename(
                {
                    "home_team": "home",
                    "away_team": "away",
                },
                axis=1,
            )
            df["season"] = 24
            return df


class FutureBetScraper(BetScraper):
    """
    Bet scraper for future odds.
    """

    @property
    def odds_endpoint(self):
        """
        The odds endpoint for future odds scrape.
        """
        return (
            BetScraper.BASE_URL
            + f"{BetScraper.SPORT}/odds/?apiKey={BetScraper.API_KEY}&"
            f"regions={BetScraper.REGIONS}&markets={BetScraper.MARKETS}"
        )


class HistoricalBetScraper(BetScraper):
    """
    Bet scraper for historical odds.
    """

    def __init__(self, date):
        """
        Initializes an instance of HistoricalBetScraper.

        Args:
            date (str): The date in YYMMDD format.

        Raises:
            Exception: If the date is not a string of length 6.
        """
        BetScraper.__init__(self)
        self.date = date

    @property
    def date(self):
        """
        The date property.
        """
        return self._date

    @date.setter
    def date(self, val):
        """
        Setter for the date property.

        Args:
            val (str): The date in YYMMDD format.

        Raises:
            Exception: If the date is not a string of length 6.
        """
        try:
            assert len(val) == 6
            self._date = f"20{val[:2]}-{val[2:4]}-{val[4:]}T12:00:00Z"
        except:
            raise Exception("Date must be a str of YYMMDD")

    @property
    def odds_endpoint(self):
        """
        The odds endpoint for historical odds scrape.
        """
        return (
            BetScraper.BASE_URL + f"{BetScraper.SPORT}/odds-history/?apiKey="
            f"{BetScraper.API_KEY}&regions={BetScraper.REGIONS}&markets={BetScraper.MARKETS}&date={self.date}"
        )
