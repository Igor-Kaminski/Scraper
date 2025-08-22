# EBay scraper

from config import  PRODUCT_KEYWORDS, MY_BASE_PRICE, MY_DELIEVERY_COST
from scraper import EbayScraper
from analyser import my_listing_standing, parse_listings, print_listings
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename = "logs/scraper.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

logging.info("Logging started")

def main():
    scraper = EbayScraper()
    logging.info("Scraper Created")
    response = scraper.search(PRODUCT_KEYWORDS[0])
    
    if response.status_code == 200:
        logging.info(f"Request successful: Status {response.status_code}")
        listings = parse_listings(response.content)
        my_listing_standing(MY_BASE_PRICE,MY_DELIEVERY_COST,listings)
        #print_listings(listings)
    else:
        logging.warning(f"Request failed! Status: {response.status_code}")
        


if __name__ == "__main__":
    main()


    