# EBay scraper

from config import  PRODUCT_KEYWORDS
from scraper import EbayScraper

def main():

    scraper = EbayScraper()
    response = scraper.search(PRODUCT_KEYWORDS[0])
    
    if response.status_code == 200:
        print("Success Ebay Page found")
    else:
        print(f"Failed! Status: {response.status_code}")







if __name__ == "__main__":
    main()