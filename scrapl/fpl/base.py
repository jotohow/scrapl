"""
scraper.py

This module contains classes and methods for scraping data from the Fantasy Premier League (FPL) API.
It includes a base scraper class with common functionality and a specific scraper for general information.

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

import json
from abc import ABC, abstractmethod

import requests
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
