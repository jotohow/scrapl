"""
A high level runner to scrape all the data from the FPL API. User can either initialise with 
a list of scraper configs, or call init_all_scrapers() to initialise all scrapers.
"""

from dataclasses import dataclass
from typing import Dict, List, Literal

from tqdm import tqdm

from ..logger import setup_logger
from . import fixtures, gameweek, general, player
from .base import BaseScraper
from .return_schema import ScraperType

logger = setup_logger(__name__)


@dataclass
class ScraperConfig:
    type: Literal["general", "fixtures", "gameweek", "player"]
    idx: int = None


class FPLScraper:

    SCRAPERS = {
        "general": general.GenInfoScraper,
        "fixtures": fixtures.FixtureScraper,
        "gameweek": gameweek.GameweekScraper,
        "player": player.PlayerScraper,
    }

    def __init__(self, scraper_config: List[ScraperConfig] = None):
        """
        Initialise the scraper with a list of scraper configs.

        Args:
            scraper_config (List[ScraperConfig], optional): List of config for each scraper. Defaults to None.
        """

        if scraper_config:
            # Initialise the scrapers with the given config
            self.scrapers = [
                (
                    self.SCRAPERS[scraper.type](scraper.idx)
                    if scraper.idx is not None
                    else self.SCRAPERS[scraper.type]()
                )
                for scraper in scraper_config
            ]
        else:
            self.scrapers = []

        self.scraped_data = {
            k: ScraperType(scraper_type=k) for k in self.SCRAPERS.keys()
        }

    def _scrape(self, scraper: BaseScraper) -> Dict[str, ScraperType]:
        """
        Scrape the data for one scraper and add it to the scraped_data.

        Args:
            scraper (BaseScraper): The scraper to scrape.

        Returns:
            Dict[str, ScraperType]: The scraped data.
        """
        scraper.scrape()

        existing_sub_types = self.scraped_data[scraper.scraper_type].scraper_sub_types
        for sub_type, data in scraper.scraped_data.scraper_sub_types.items():

            # If the sub type is not in the existing sub types, add it
            if sub_type not in existing_sub_types:
                self.scraped_data[scraper.scraper_type].scraper_sub_types[
                    sub_type
                ] = data
            else:
                # If the sub type is already in the existing sub types, extend the data
                self.scraped_data[scraper.scraper_type].scraper_sub_types[
                    sub_type
                ].scraper_return_data.extend(data.scraper_return_data)
        return scraper.scraped_data

    def init_all_scrapers(self):
        """
        Initialise all scrapers.

        Returns:
            List[BaseScraper]: The list of scrapers.
        """

        # Get the general scraper and collect the ids of the players
        logger.info("Initialising all scrapers")
        gis = self.SCRAPERS["general"]()
        self.scrapers.append(gis)
        logger.info("Scraping general info")
        self._scrape(gis)

        # Get the ids of the players and initialise the player scrapers
        elements = gis.scraped_data.scraper_sub_types["element_map"].scraper_return_data
        _scrapers = [player.PlayerScraper(el) for el in elements[0]]
        self.scrapers.extend(_scrapers)

        # Get the ids of the fixtures and initialise the fixture scrapers
        self.scrapers.append(fixtures.FixtureScraper())
        return self.scrapers

    def scrape(self):
        """
        Scrape with all instantiated scrapers.
        """
        if not self.scrapers:
            raise ValueError(
                "No scrapers given. Either initialise with specific scraper values, or call"
                " init_all_scrapers() to initialise all scrapers."
            )

        scraper_tqdm = tqdm(self.scrapers)
        scraper_tqdm.set_description("Scraping all scrapers")
        for scraper in scraper_tqdm:
            if not scraper.scraped:
                self._scrape(scraper)
        return self.scraped_data
