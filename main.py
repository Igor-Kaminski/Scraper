# EBay scraper

from config import  PRODUCT_KEYWORDS
from scraper import EbayScraper
from analyser import parse_listings, print_listings

def main():
    scraper = EbayScraper()
    response = scraper.search(PRODUCT_KEYWORDS[0])
    
    if response.status_code == 200:
        listings = parse_listings(response.content)
        print_listings(listings)
    else:
        print(f"Failed! Status: {response.status_code}")


if __name__ == "__main__":
    main()


    