'''
Analyser of HTML
'''

from bs4 import BeautifulSoup
from plyer import notification
import logging
import re
from monitor.config import NOTIFICATION_TITLE, NOTIFICATION_MESSAGE, NOTIFICATION_TIMEOUT


def clean_price(price_text):
    if not price_text:
        return None
    price_text = price_text.replace(' ', '')
    match = re.search(r'\d+\.?\d*', price_text)
    if match:
        return float(match.group())
    return None

def parse_listings(html):
    soup = BeautifulSoup(html, 'lxml')
    listings = []
    seen = set()
    junk_keywords = ['Shop on eBay', 'Unit']


    for card in soup.select('.su-card-container'):
        title_el = card.select_one('.su-styled-text.secondary.large')
        price_el = card.select_one('.su-styled-text.primary.bold.large-1.s-card__price')
        delivery_el = card.select_one('.su-styled-text.secondary.large')  # update if different
        if title_el and price_el:
            title = title_el.get_text(strip=True)
            if any(k.lower() in title.lower() for k in junk_keywords):
                continue
            price = clean_price(price_el.get_text(strip=True))
            
            url = None
            link_el = card.find('a', href=True)
            if not link_el:
                link_el = card.select_one('a[href*="/itm/"]')
            if link_el:
                href = link_el.get('href')
                if href and '/itm/' in href:
                    if href.startswith('/'):
                        url = f"https://www.ebay.co.uk{href}"
                    elif href.startswith('http'):
                        url = href
            
            delivery_price = 0.0
            if delivery_el:
                delivery_text = delivery_el.get_text(strip=True).lower()
                if 'free' in delivery_text:
                    delivery_price = 0.0
                else:
                    delivery_price = clean_price(delivery_text) or 0.0

            total_price = price + delivery_price

            if title not in seen:
                listings.append({'title': title, 'price': total_price, 'url': url})
                seen.add(title)
                logging.debug(f"Added listing: {title} — £{total_price:.2f}")

    for item in soup.select('.s-item'):
        title_el = item.select_one('.s-item__title')
        price_el = item.select_one('.s-item__price')
        delivery_el = item.select_one('.s-item__shipping')  
        if title_el and price_el:
            title = title_el.get_text(strip=True)
            if any(k.lower() in title.lower() for k in junk_keywords):
                continue
            price = clean_price(price_el.get_text(strip=True))
            
            url = None
            link_el = item.find('a', href=True)
            if link_el:
                href = link_el.get('href')
                if href.startswith('/'):
                    url = f"https://www.ebay.co.uk{href}"
                elif href.startswith('http'):
                    url = href
            
            delivery_price = 0.0
            if delivery_el:
                delivery_text = delivery_el.get_text(strip=True).lower()
                if 'free' in delivery_text:
                    delivery_price = 0.0
                else:
                    delivery_price = clean_price(delivery_text) or 0.0

            total_price = price + delivery_price

            if title not in seen:
                listings.append({'title': title, 'price': total_price, 'url': url})
                seen.add(title)
                logging.debug(f"Added listing: {title} — £{total_price:.2f}")

    listings.sort(key=lambda x: x['price'])
    logging.info(f"Total listings parsed: {len(listings)}")

    return listings

def print_listings(listings):
    if not listings:
        print("No listings found.")
        return
    for i, listing in enumerate(listings, 1):
        if listing.get('url'):
            item_id = listing['url'].split('/itm/')[-1].split('?')[0] if '/itm/' in listing['url'] else "Link"
            url_text = f" | 🔗 {item_id}"
        else:
            url_text = ""
        print(f"{i}. {listing['title']} — £{listing['price']:.2f}{url_text}")

def my_listing_standing(MY_BASE_PRICE, MY_DELIEVERY_COST, listings, product_name, links_log_path=None):
    if not listings:
        print(f"No listings found for {product_name}")
        logging.error(f"No listings found for {product_name} | comparison between your cheapest product unsuccessful")
        return

    cheaper_listings = []
    real_price = float(MY_BASE_PRICE + MY_DELIEVERY_COST)
    
    for x in listings:
        if x["price"] < real_price:
            cheaper_listings.append(x)
    
    if len(cheaper_listings) > 0:
        logging.info(f"{len(cheaper_listings)} cheaper listings found for {product_name}")
        print(f"Cheaper listings have been found for {product_name}:\n")
        
        if links_log_path:
            try:
                with open(links_log_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n=== {product_name} - {len(cheaper_listings)} cheaper listings found ===\n")
                    for i, listing in enumerate(cheaper_listings, 1):
                        if listing.get('url'):
                            f.write(f"{i}. {listing['title']} — £{listing['price']:.2f} | {listing['url']}\n")
                        else:
                            f.write(f"{i}. {listing['title']} — £{listing['price']:.2f} | No URL\n")
                    f.write("=" * 60 + "\n")
            except Exception as e:
                logging.error(f"Failed to write links log: {e}")
        
        notification.notify(
            title=f"{NOTIFICATION_TITLE} - {product_name}",
            message=NOTIFICATION_MESSAGE.format(count=len(cheaper_listings)),
            timeout=NOTIFICATION_TIMEOUT
        )
            
        for i, listing in enumerate(cheaper_listings, 1):
            logging.info(f"Cheaper listing {i} for {product_name}: {listing['title']} — £{listing['price']:.2f}")
            print(f"{i}. {listing['title']} — £{listing['price']:.2f}")
    else:
        logging.info(f"No cheaper listings found for {product_name}")
        print(f"None were lower lets go! ({product_name})")
