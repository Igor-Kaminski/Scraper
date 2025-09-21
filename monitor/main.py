# EBay scraper

from monitor.config import PRODUCTS, SCHEDULER, CHECK_INTERVAL
from monitor.scraper import EbayScraper
from monitor.analyser import my_listing_standing, parse_listings, print_listings
import logging
import os
import time
import signal
import sys
import asyncio


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

LOG_DIR = os.path.join(REPO_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'scraper.log'),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

logging.info("Logging started")

LINKS_LOG_FILE = os.path.join(LOG_DIR, 'scraper_links.log')

async def run_once():
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
        html, status = await scraper.search(keywords)
        
        if status == 200:
            logging.info(f"Request successful for {product['name']}: Status {status}")
            listings = parse_listings(html)
            my_listing_standing(product['my_price'], product['delivery_cost'], listings, product['name'], LINKS_LOG_FILE)
            #print_listings(listings)
        else:
            logging.warning(f"Request failed for {product['name']}! Status: {status}")
            print(f"Failed to check {product['name']}")

async def run_daemon():
    logging.info(f"Starting async daemon - checking every {CHECK_INTERVAL} seconds")
    print(f"Starting async daemon - checking every {CHECK_INTERVAL} seconds")
    
    while True:
        try:
            await run_once()
            logging.info(f"Cycle complete. Sleeping for {CHECK_INTERVAL} seconds...")
            await asyncio.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            logging.info("Daemon stopped by user")
            print("Daemon stopped by user")
            break
        except Exception as e:
            logging.error(f"Error in daemon loop: {e}")
            print(f"Error: {e} - retrying in 60 seconds")
            await asyncio.sleep(60)

def signal_handler(sig, frame):
    logging.info("Received shutdown signal (Ctrl+C)")
    print("\nShutting down gracefully...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    if SCHEDULER:
        asyncio.run(run_daemon())
    else:
        asyncio.run(run_once())

if __name__ == "__main__":
    main()


    