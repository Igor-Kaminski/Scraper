# EBay scraper

from config import PRODUCTS, SCHEDULER, CHECK_INTERVAL
from scraper import EbayScraper
from analyser import my_listing_standing, parse_listings, print_listings
import logging
import os
import time
import signal
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(SCRIPT_DIR, 'logs')

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'scraper.log'),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

logging.info("Logging started")

LINKS_LOG_FILE = os.path.join(LOG_DIR, 'scraper_links.log')

def signal_handler(sig, frame):
    logging.info("Received shutdown signal (Ctrl+C)")
    print("\nShutting down gracefully...")
    sys.exit(0)

def run_once():
    scraper = EbayScraper()
    logging.info("Scraper Created")
    
    # Multi-product mode
    for product in PRODUCTS:
        if not product.get('enabled', True):
            logging.info(f"Skipping disabled product: {product['name']}")
            continue
            
        logging.info(f"Checking product: {product['name']}")
        print(f"Checking product: {product['name']}")
        
        # Use first keyword for search
        keywords = product['keywords'][0] if product['keywords'] else product['name']
        response = scraper.search(keywords)
        
        if response.status_code == 200:
            logging.info(f"Request successful for {product['name']}: Status {response.status_code}")
            listings = parse_listings(response.content)
            my_listing_standing(product['my_price'], product['delivery_cost'], listings, product['name'], LINKS_LOG_FILE)
            #print_listings(listings)
        else:
            logging.warning(f"Request failed for {product['name']}! Status: {response.status_code}")
            print(f"Failed to check {product['name']}")

def run_daemon():
    logging.info(f"Starting daemon mode - checking every {CHECK_INTERVAL} seconds")
    print(f"Starting daemon mode - checking every {CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            logging.info("Starting price check cycle...")
            print("Checking prices...")
            
            scraper = EbayScraper()
            
            # Multi-product mode
            for product in PRODUCTS:
                if not product.get('enabled', True):
                    logging.info(f"Skipping disabled product: {product['name']}")
                    continue
                    
                logging.info(f"Checking product: {product['name']}")
                print(f"Checking product: {product['name']}")
                
                # Use first keyword for search
                keywords = product['keywords'][0] if product['keywords'] else product['name']
                response = scraper.search(keywords)
                
                if response.status_code == 200:
                    logging.info(f"Request successful for {product['name']}: Status {response.status_code}")
                    listings = parse_listings(response.content)
                    my_listing_standing(product['my_price'], product['delivery_cost'], listings, product['name'], LINKS_LOG_FILE)
                else:
                    logging.warning(f"Request failed for {product['name']}! Status: {response.status_code}")
                    print(f"Failed to check {product['name']}")
            
            logging.info(f"Price check complete. Next check in {CHECK_INTERVAL} seconds")
            print(f"Next check in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logging.info("Daemon stopped by user")
            print("\nDaemon stopped by user")
            break
        except Exception as e:
            logging.error(f"Error in daemon loop: {e}")
            print(f"Error: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    if SCHEDULER:
        run_daemon()
    else:
        run_once()
        


if __name__ == "__main__":
    main()


    