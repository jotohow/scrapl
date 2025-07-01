from tqdm import tqdm

import scrapl.fpl.scraper as scraper


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
    scraped_data["player_stats"] = []

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
        if "player_stats" in list(d.keys())[0]:
            scraped_data["player_stats"].extend(list(d.values())[0])
        else:
            scraped_data.update(d)

    return scraped_data


if __name__ == "__main__":
    # Example usage
    scraped_data = run_scrapers(elements=[1, 2])
    print(scraped_data["player_stats"])
