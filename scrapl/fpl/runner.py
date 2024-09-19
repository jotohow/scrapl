from tqdm import tqdm
import fpl.scraper as scraper


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
    gis = scraper.GenInfoScraper()
    scraped_data = gis.scrape()

    # Extract player ids from general info
    elements = scraped_data["element_map"].keys() if not elements else elements
    n_players = len(elements)
    scrapers = [scraper.PlayerScraper(el) for el in elements]
    scrapers = scrapers + [scraper.FixtureScraper()]

    # Run the player and fixture scrapers
    scraper_tqdm = tqdm(scrapers)
    scraper_tqdm.set_description(f"Scraping fixtures and {n_players} players")
    scraped_data_ = [scraper.scrape() for scraper in scraper_tqdm]
    for d in scraped_data_:
        scraped_data.update(d)

    return scraped_data
