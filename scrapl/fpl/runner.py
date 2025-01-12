from tqdm import tqdm

from scrapl.fpl import fixtures, general, player


def run_scrapers(elements=[]):
    """
    Run the scrapers to retrieve data for players and fixtures.

    Args:
        elements (list, optional): A list of player elements to scrape.
            If not provided, all player elements will be scraped. Defaults
            to [].

    Returns:
        dict: A dictionary containing the scraped data.
    """

    # Scrape general info
    gis = general.GenInfoScraper()
    scraped_data = gis.scrape()

    # Extract player ids from general info
    elements = scraped_data["element_map"].keys() if not elements else elements
    n_players = len(elements)
    scrapers = [player.PlayerScraper(el) for el in elements]
    scrapers = scrapers + [fixtures.FixtureScraper()]

    # Run the player and fixture scrapers
    scraper_tqdm = tqdm(scrapers)
    scraper_tqdm.set_description(f"Scraping fixtures and {n_players} players")
    scraped_data_ = [scraper.scrape() for scraper in scraper_tqdm]
    for d in scraped_data_:
        scraped_data.update(d)

    return scraped_data
