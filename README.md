# scrapl

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![GitHub Issues](https://img.shields.io/github/issues/jth500/scrapl)

A Python package to scrape Premier League (ScraPL) data from the Fantasy Premier League (FPL) and [The Odds API](https://the-odds-api.com/).

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Advanced Examples](#advanced-examples)
- [Contributing](#contributing)
- [License](#license)
- [Community](#community)

## About

`scrapl` is designed to help developers easily access and extract data from the Fantasy Premier League and The Odds API. Whether you're building analytics tools, fantasy league optimizers, or integrating sports data into your applications, `scrapl` provides the necessary tools to get you started quickly.

This package was developed for use in [lionel](https://github.com/jth500/lionel), but it can be utilized independently for various data scraping needs related to the Premier League.

## Features

- **FPL Data Scraping**: Retrieve player statistics, team information, and gameweek data from the Fantasy Premier League API.
- **Odds Data Integration**: Access betting odds and related data from The Odds API.
- **Modular Design**: Easily integrate specific scrapers based on your project needs.
- **Type Enforcement**: Ensures return types for better code reliability and maintainability.

## Installation

You can install `scrapl` directly from GitHub using `pip`:

```bash
pip install git+https://github.com/jth500/scrapl.git
```

### Dependencies

Ensure you have the following dependencies installed:

You can install all dependencies using:

```bash
pip install git+https://github.com/jth500/scrapl.git
```

## Usage

### Basic Usage

#### Scraping Player Statistics for a Specific Player

To extract statistics for a specific player across all gameweeks in the current season:

```python
from scrapl.fpl.scraper import PlayerScraper

# Initialize the scraper with the player ID (element)
player_id = 1
player_scraper = PlayerScraper(player_id)

# Perform the scraping
player_stats = player_scraper.scrape()

print(player_stats)
# Output:
# {
#     'player_stats_1': [
#         {'element': 1, 'gameweek': 1, 'points': 5, ...},
#         {'element': 1, 'gameweek': 2, 'points': 7, ...},
#         ...
#     ]
# }
```

### Advanced Examples

FPLScraper runs each type of scraper. Users can define specific types of scrape with config, or scrape everything by default.

```python
from scrapl.fpl.scraper import FPLScraper

# Either initialize the runner with a configs for each scraper. If none are given, everything is scraped
scraper_configs = None # [{"type":"player", "idx": 1}, ...]

scraper = FPLScraper(scraper_configs)

# Perform the scraping
scraper.init_all_scrapers()
data = scraper.scrape()

print(data)
# Example Output:
# {
#    "general": {"gw_deadlines": [...], "element_name_map": [...], "teams": [...]}
#    "players": {"players": []},
#    ...
# }
#
```

#### Scraping Odds Data from The Odds API

TODO: Add documentation

To integrate betting odds data into your application:

## Contributing

Contributions are welcome!

1. **Fork the Repository**
2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add Your Feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE).

## Community

- **Issues**: If you encounter any issues or have questions, feel free to [open an issue](https://github.com/jth500/scrapl/issues).
- **Contributions**: Contributions are welcomed and appreciated. Check out the [Contributing](#contributing) section for more details.
