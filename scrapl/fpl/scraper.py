from dataclasses import dataclass, field
from typing import List, Literal, Union

from tqdm import tqdm

from ..logger import setup_logger
from . import fixtures, gameweek, general, player

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

        if scraper_config:
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

        self.scraped_data = {k: [] for k in self.SCRAPERS.keys()}

    def init_all_scrapers(self):

        # Get the general scraper and collect the ids of the players
        logger.info("Initialising all scrapers")
        gis = self.SCRAPERS["general"]()
        self.scrapers.append(gis)
        logger.info("Scraping general info")
        gis.scrape()  # sets its scrape value to True
        elements = gis.scraped_data["element_map"].keys()
        _scrapers = [player.PlayerScraper(el) for el in elements]
        self.scrapers.extend(_scrapers)
        self.scrapers.append(fixtures.FixtureScraper())
        return self.scrapers

    # Noting that each scraper may return slightly different data strucutre. E.g. general will return a dict with
    # team map, element map. gameweek will just be a list of player stats. What is a good way to handle this?
    # I need to have an overarching return data structure works for all types of scrapers. The general one is the most general. Let's focus on that.
    # This returns team map, element map, player map. It returns one for each.
    # So I need to account for each scraper returning a different TYPE of data, and different numbers of the SAME TYPE of data.
    # I think the best way to do this is to have a dict of lists.

    # each scraper will return {type_of_data1: [{}, {}]}, {type_of_data2: [{}, {}]}, {type_of_data3: [{}, {}]}

    # BUT: This doesn't account for player/gameweek, where multiple scrapers will return the same type of data, which should really
    # be in the same list...

    # Yeah, I think
    """
    {
        "general": {
            "team_map": [],
            "element_map": [],
            "gw_deadlines": [],
        },
        "player": {"player": []},
        "gameweek": {"gameweek": []}},
        "fixture": {"fixture": []},
    }


    # Yep. I think this is right. Need to have type (scraper), subtype (return type), then list of data 

    # so each scraper should return {"team_map/player": []}
    
    
    """

    def scrape(self):
        if not self.scrapers:
            raise ValueError(
                "No scrapers given. Either initialise with specific scraper values, or call"
                " init_all_scrapers() to initialise all scrapers."
            )

        scraper_tqdm = tqdm(self.scrapers)
        scraper_tqdm.set_description("Scraping all scrapers")
        for scraper in scraper_tqdm:
            if not scraper.scraped:
                self.scraped_data[scraper.scraper_type] = scraper.scrape()
                # self.scraped_data.update(scraper.scrape())
        return self.scraped_data
