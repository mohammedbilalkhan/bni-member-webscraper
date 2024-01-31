# bni-region-webscraper

```markdown
# Web Scraping BNI Region Names with Selenium

This Python script utilizes Selenium to scrape BNI (Business Network International) region names from a webpage and stores them into a CSV file.

## Prerequisites
- Python 3 installed on your machine.
- Selenium library installed (`pip install selenium`).
- Chrome WebDriver installed and added to PATH.

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/bni-region-scraper.git
cd bni-region-scraper
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Ensure you have a CSV file ready with a "Region Name" column.
2. Update the `config.py` file with your CSV file name.
3. Run the script:
   ```bash
   python scrape_bni_regions.py
   ```
4. The script will launch a Chrome browser, scrape the region names from the BNI webpage, and save them to the specified CSV file.

## Configuration

In `config.py`, you can adjust the following parameters:
- `CSV_FILE`: The name of your CSV file.
- `URL`: The URL of the BNI webpage containing the region names.

## Example CSV File

Here's an example of how your CSV file should look:

```
| Region Name |
|-------------|
| Region 1    |
| Region 2    |
| Region 3    |
| ...         |
```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Remember to replace `yourusername` in the clone URL with your actual GitHub username.
