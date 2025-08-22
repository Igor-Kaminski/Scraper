'''
Analyser of HTML
'''

import enum
from bs4 import BeautifulSoup

import re

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
            
            delivery_price = 0.0
            if delivery_el:
                delivery_text = delivery_el.get_text(strip=True).lower()
                if 'free' in delivery_text:
                    delivery_price = 0.0
                else:
                    delivery_price = clean_price(delivery_text) or 0.0

            total_price = price + delivery_price

            if title not in seen:
                listings.append({'title': title, 'price': total_price})
                seen.add(title)

    for item in soup.select('.s-item'):
        title_el = item.select_one('.s-item__title')
        price_el = item.select_one('.s-item__price')
        delivery_el = item.select_one('.s-item__shipping')  
        if title_el and price_el:
            title = title_el.get_text(strip=True)
            if any(k.lower() in title.lower() for k in junk_keywords):
                continue
            price = clean_price(price_el.get_text(strip=True))
            
            delivery_price = 0.0
            if delivery_el:
                delivery_text = delivery_el.get_text(strip=True).lower()
                if 'free' in delivery_text:
                    delivery_price = 0.0
                else:
                    delivery_price = clean_price(delivery_text) or 0.0

            total_price = price + delivery_price

            if title not in seen:
                listings.append({'title': title, 'price': total_price})
                seen.add(title)

    listings.sort(key=lambda x: x['price'])
    return listings

def print_listings(listings):
    if not listings:
        print("No listings found.")
        return
    for i, listing in enumerate(listings, 1):
        print(f"{i}. {listing['title']} — £{listing['price']:.2f}")

def my_listing_standing(MY_BASE_PRICE, MY_DELIEVERY_COST, listings):
    cheaper_listings = []
    real_price = float(MY_BASE_PRICE + MY_DELIEVERY_COST)
    
    for x in listings:
        if x["price"] < real_price:
            cheaper_listings.append(x)
    if len(cheaper_listings) > 0:
        print("Cheaper listings have been found:\n")
        for i, listing in enumerate(cheaper_listings, 1):
            print(f"{i}. {listing['title']} — £{listing['price']:.2f}")
    else:
        print("None were lower lets go!")
        