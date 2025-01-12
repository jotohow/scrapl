# scrapl

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![GitHub Issues](https://img.shields.io/github/issues/jth500/scrapl)

A Python package to scrape Premier League (ScraPL) data from the Fantasy Premier League (FPL) and [The Odds API](https://the-odds-api.com/).

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Example Usage](#example-usage)
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

or clone the repo

## Example Usage

### 1. Basic Usage

This example showcases how to perform a simple scrape of general information and fixtures using the `FPLScraper` class. It initializes the scraper with a minimal configuration, runs the scraping process, and saves the results to a JSON file.

```python
"""
Basic Usage Example

This script demonstrates how to initialize the FPLScraper with a specific list of scrapers,
perform the scraping, and save the scraped data to a JSON file.
"""

import os
from scrapl.fpl.scraper import FPLScraper, ScraperConfig

def main():
    # Define a minimal set of scrapers to initialize: "general" and "fixtures"
    scraper_config = [
        ScraperConfig(scraper_type="general"),
        ScraperConfig(scraper_type="fixtures"),
    ]

    # Initialize the FPLScraper with the specified configuration
    fpl_scraper = FPLScraper(scraper_config=scraper_config)

    # Run the scraping process
    scraped_data = fpl_scraper.scrape()

    # Display the top-level keys of the scraped data
    print("Scraped data keys:", scraped_data.keys())

    # Save the scraped data to a JSON file within the examples directory
    output_file = os.path.join("scrapl", "examples", "output_basic_usage.json")
    fpl_scraper.to_json(output_file)
    print(f"Saved scraped data to {output_file}")

    # Optionally, clear the scraped data from memory
    fpl_scraper.clear_data()
    print("Data cleared. Current stored data:", fpl_scraper.scraped_data)

if __name__ == "__main__":
    main()
```


**Running the Script:**

1. **Ensure Dependencies Are Installed**:  
   Make sure you have all required packages installed, such as `tqdm`.

2. **Navigate to the Project Root**:  
   Open your terminal and navigate to the root directory of your project where the `scrapl/` package resides.

3. **Execute the Script**:  
   Run the script using Python:
   ```bash
   python -m src.examples.example_basic_usage
   ```

4. **Verify Output**:  
   After execution, check the `scrapl/examples/output_basic_usage.json` file to see the scraped data.


### 2. Advanced Examples

For more comprehensive demonstrations, see the scripts provided in the [`examples/`](scrapl/examples/) directory of this repository.

**Available Examples:**

- **`example_init_all.py`**:  
  Demonstrates how to initialize and scrape data using all available scrapers, including dependent scrapers like individual player data.

- **`example_custom_scraper.py`**:  
  Shows how to create and register a custom scraper, integrate it with the `FPLScraper`, and execute the scraping process.

- **`example_basic_usage.py`**:  
  (As detailed above) Provides a basic usage scenario for quick starts.

**How to Access and Run Advanced Examples:**

1. **Navigate to the root dir**:


3. **Run an Example Script**:
   For instance, to run the advanced script that initializes all scrapers:
   ```bash
   python -m scrapl.examples.example_init_all
   ```

4. **Review the Output**:  
   Each script will save its scraped data to a corresponding JSON file within the `examples/` directory and print relevant information to the console.


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
