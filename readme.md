# Noon Laptops Scraping

## Overview

This Python script scrapes laptop information from the Noon website, including details such as brand, model, price, stock, and specifications. The scraped data is saved in both CSV and SQLite formats.

## Purpose

The purpose of this script is to collect information about laptops available on the Noon website, including details such as brand, model, price, stock, and specifications.

## Dependencies

- Python 3.x
- `requests-html` library
- `pandas` library
- `sqlite3` module (part of the Python standard library)

## Usage

1. Clone the Git repository:

   ```
   bashCopy code
   git clone https://github.com/ahmedmgelwan/noon-laptops-scraping.git
   ```

2. Navigate to the project directory:

   ``` bash
   cd noon-laptops-scraping
   ```

3. Install the required dependencies:

   ``` bash
   pip install -r requirements.txt
   ```

4. Run the script:

   ``` bash
   python scrape_laptops.py
   ```

5. The scraped data will be saved in both CSV (`noon-laptops.csv`) and SQLite (`noon-laptops.db`) formats in the project directory.

## Notes

- Adjustments can be made to the script for customization based on specific requirements or changes in the website structure.

- Error handling and logging are implemented for improved robustness. Check the `scraping.log` file for any encountered errors during the scraping process.

- The script includes user-agent headers to mimic a real web browser for preventing server blocks.

  