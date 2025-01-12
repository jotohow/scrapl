"""
A high level runner to scrape all the data from the FPL API. User can either initialise with 
a list of scraper configs, or call init_all_scrapers() to initialise all scrapers.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Type

from tqdm import tqdm

from ..logger import setup_logger
from . import fixtures, gameweek, general, player
from .base import FPLScraperBase
from .return_schema import ScraperType

logger = setup_logger(__name__)


@dataclass
class ScraperConfig:
    scraper_type: Literal["general", "fixtures", "gameweek", "player"]
    idx: Optional[int] = None


class FPLScraper:
    """
    A high-level runner class that coordinates various scrapers for the FPL API.
    """

    SCRAPERS: Dict[str, Type[FPLScraperBase]] = {
        "general": general.GenInfoScraper,
        "fixtures": fixtures.FixtureScraper,
        "gameweek": gameweek.GameweekScraper,
        "player": player.PlayerScraper,
    }

    def __init__(self, scraper_config: Optional[List[ScraperConfig]] = None):
        """
        Initialise the scraper runner with a list of scraper configurations,
        or create an empty container for scrapers which can be populated later.

        Args:
            scraper_config (List[ScraperConfig], optional):
                List of config for each scraper. Defaults to None.
        """
        self.scrapers: List[FPLScraperBase] = []
        if scraper_config:
            self._init_scrapers_from_config(scraper_config)

        self.scraped_data: Dict[str, Dict[str, list]] = defaultdict(
            lambda: defaultdict(list)
        )

    def _init_scrapers_from_config(self, scraper_config: List[ScraperConfig]) -> None:
        """
        Create scraper instances based on a list of scraper configurations.
        """
        for config in scraper_config:
            cls = self.SCRAPERS[config.scraper_type]
            self.scrapers.append(cls(config.idx) if config.idx is not None else cls())

    def register_scraper(self, name: str, scraper_class: Type[FPLScraperBase]) -> None:
        """
        Register a new scraper class for a given name.

        Args:
            name (str): Unique name/key for the scraper
            scraper_class (Type[FPLScraperBase]): The class object of the scraper
        """
        self.SCRAPERS[name] = scraper_class
        logger.info(f"Registered new scraper: {name}")

    def _merge_scraped_data(
        self, scraper_type: str, new_data: Dict[str, ScraperType]
    ) -> None:
        """
        Merge newly scraped data into self.scraped_data.

        Args:
            scraper_type (str): The string identifier for the scraper type
            new_data (Dict[str, ScraperType]):
                The dictionary of sub_types -> ScraperType from the scraper
        """
        for sub_type, data_wrapper in new_data.items():
            # data_wrapper.scraper_return_data is assumed to be a list or list-like
            self.scraped_data[scraper_type][sub_type].extend(
                data_wrapper.scraper_return_data
            )

    def _scrape_single(self, scraper: FPLScraperBase) -> Dict[str, ScraperType]:
        """
        Run a single scraper and merge the results into the global store.

        Args:
            scraper (FPLScraperBase): The scraper to run.

        Returns:
            Dict[str, ScraperType]: The newly scraped data.
        """
        scraper.scrape()
        self._merge_scraped_data(
            scraper.scraper_type, scraper.scraped_data.scraper_sub_types
        )
        return scraper.scraped_data.scraper_sub_types

    def init_all_scrapers(self) -> List[FPLScraperBase]:
        """
        Initialise default scrapers that gather all relevant data.
        This method does not scrape them immediately (but does scrape
        the 'general' info to retrieve IDs of players for PlayerScrapers).

        Returns:
            List[FPLScraperBase]: The list of initialized scrapers.
        """
        logger.info("Initializing all scrapers")

        # Always start with the General Info Scraper to get player data
        if not any(isinstance(s, general.GenInfoScraper) for s in self.scrapers):
            gen_scraper = self.SCRAPERS["general"]()
            self.scrapers.append(gen_scraper)

            logger.info("Scraping general info to retrieve IDs for dependent scrapers.")
            self._scrape_single(gen_scraper)

            # Once we have the IDs, create the PlayerScrapers
            elements = gen_scraper.scraped_data.scraper_sub_types[
                "element_map"
            ].scraper_return_data
            player_scrapers = [player.PlayerScraper(el) for el in elements[0]]
            self.scrapers.extend(player_scrapers)

        # Add the FixtureScraper if not already present
        if not any(isinstance(s, fixtures.FixtureScraper) for s in self.scrapers):
            self.scrapers.append(self.SCRAPERS["fixtures"]())

        # Additional scrapers can be appended in similar fashion...
        return self.scrapers

    def scrape(self) -> Dict[str, Dict[str, list]]:
        """
        Scrape data using all currently instantiated scrapers.
        If a scraper has already been scraped, it won't be re-run.

        Returns:
            Dict[str, Dict[str, list]]: Nested dictionary of {scraper_type -> {sub_type -> data}}
        """
        if not self.scrapers:
            raise ValueError(
                "No scrapers available. Either instantiate the class with a config "
                "or call init_all_scrapers() to initialize default scrapers."
            )

        # Show progress bar for convenience
        for scraper in tqdm(self.scrapers, desc="Scraping all scrapers"):
            if not scraper.scraped:  # if it hasn't been run yet
                self._scrape_single(scraper)

        return dict(self.scraped_data)  # don't return the mutable default dict

    def clear_data(self) -> None:
        """
        Clear all currently stored scraped data.
        """
        self.scraped_data.clear()
        for s in self.scrapers:
            s.scraped = False
        logger.info("Cleared all scraped data.")
