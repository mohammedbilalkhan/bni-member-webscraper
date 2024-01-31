
# BNI Member Details Web Scraping with Selenium

This repository contains a Python script for web scraping BNI (Business Network International) member details using Selenium. The script is designed to extract all the information such as members name, phone, email, company name, speciality, company address, and business detail from the BNI website and organize it into a CSV file based on the specified region names.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3
- Selenium
- ChromeDriver (for Chrome browser)

Install the required Python libraries using:

```bash
pip install selenium
```

Download the appropriate web driver for your browser and set the path in the script.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/mohammedbilalkhan10/bni-members-webscraper.git
cd bni-members-webscraper
```

2. Edit the `regions.csv` file with the specific region names under the "Region" column.

3. Run the script:

```bash
python scraper_bni_members.py
```

The script will launch a browser, navigate to the BNI website, and start scraping member details for each specified region. The information will be saved in a CSV file named '{logpath}/{region}/{chaptername}_MemberDetails.csv'.


## Acknowledgments

- The script utilizes Selenium for web scraping.
- Special thanks to the BNI community for their valuable information.

Happy scraping!
