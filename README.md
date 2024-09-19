# scrapl
A Python package to scrape Premier League (ScraPL) data from the Fantasy Premier League and The Odds API.

## Index

- [About](#about)
- [Usage](#usage)
- [Community](#community)

## About
scrapl includes scraper code for the FPL API and [The Odds API](https://the-odds-api.com/). It was developed for use in [lionel](https://github.com/jth500/lionel).

## Usage
Instructions

### Installation
Install from git using pip install

```
pip install git+https://github.com/jth500/scrapl.git
```

### Example usage

To extract stats for a specific player for every gameweek of the current season:
```
from scrapl.fpl.scraper import PlayerScraper

element = 1
ps = PlayerScraper(element)

ps.scrape()
# {'player_stats_1': [{'element': 1,...
```

To extract player and fixture data for the present season:
```
from scrapl.fpl.runner import run_scrapers

# Player IDs - if not provided all players will be scraped by default
elements = [1, 2, 3]
data = run_scrapers(elements)

# Scraping fixtures and 3 players: 100%|██████████| 4/4 [00:00<00:00, 23.97it/s]
```

## Community

- Contributions are welcomed and appreciated.
- Licence: MIT