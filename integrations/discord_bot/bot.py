from monitor import EbayScraper, parse_listings, PRODUCTS
from dotenv import load_dotenv
import discord
import os



# ----------------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------------
load_dotenv()


RUN_CHANNEL_ID = 1237588480985534484
LOG_CHANNEL_ID = 1418641605149196409
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')


def start_scraper_once():
    scraper = EbayScraper()
    messages = []

    for product in PRODUCTS:
        if not product.get('enabled', True):
            continue

        messages.append(f"Checking product: {product['name']}")
        
        keywords = product['keywords'][0] if product['keywords'] else product['name']
        response = scraper.search(keywords)
        
        if response.status_code == 200:
            listings = parse_listings(response.content)
            result_msgs = my_listing_standing(
                product['my_price'],
                product['delivery_cost'],
                listings,
                product['name']
            )
            messages.extend(result_msgs)
        else:
            messages.append(f"Failed to check {product['name']} (status {response.status_code})")
    
    return messages

def my_listing_standing(MY_BASE_PRICE, MY_DELIVERY_COST, listings, product_name):
    if not listings:
        return [f"No listings found for {product_name}"]

    cheaper_listings = []
    real_price = float(MY_BASE_PRICE + MY_DELIVERY_COST)
    
    for x in listings:
        if x["price"] < real_price:
            cheaper_listings.append(x)
    
    messages = []
    if cheaper_listings:
        messages.append(f"{len(cheaper_listings)} cheaper listings found for {product_name}:")
        for i, listing in enumerate(cheaper_listings, 1):
            line = f"{i}. {listing['title']} — £{listing['price']:.2f}"
            if listing.get('url'):
                line += f" | {listing['url']}"
            messages.append(line)
    else:
        messages.append(f"No cheaper listings found for {product_name} (your price is lowest!)")
    
    return messages

def start_daemon():
    pass  


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
        messages = start_scraper_once()
        result_block = "\n".join(messages)

        if len(result_block) <= 1900:
            await message.channel.send(f"\n{result_block}\n")
        else:
            for i in range(0, len(result_block), 1900):
                chunk = result_block[i:i+1900]
                await message.channel.send(f"\n{chunk}\n")

        await message.channel.send('Price check complete!')

    if message.content.lower().startswith('!daemon'):
        start_daemon()        


def main():
    client.run(DISCORD_BOT_TOKEN)