from monitor import EbayScraper, parse_listings, PRODUCTS
from dotenv import load_dotenv
import discord
import os
import logging



# ----------------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------------
load_dotenv()


RUN_CHANNEL_ID = 1237588480985534484
LOG_CHANNEL_ID = 1418641605149196409
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')


def start_scraper_once():
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


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    run_channel = client.get_channel(RUN_CHANNEL_ID)
    log_channel = client.get_channel(LOG_CHANNEL_ID)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!check'):
        await message.channel.send('Running price check...')
        start_scraper()

client.run(DISCORD_BOT_TOKEN)