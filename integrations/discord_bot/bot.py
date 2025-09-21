'''
Discord bot with scraper logic
'''


from monitor import EbayScraper, parse_listings, PRODUCTS, RUN_CHANNEL_ID, LOG_CHANNEL_ID, DISCORD_BOT_TOKEN, CHECK_INTERVAL
import discord
import asyncio


async def start_scraper_once():
    scraper = EbayScraper()
    messages = []

    for product in PRODUCTS:
        if not product.get('enabled', True):
            continue

        messages.append(f"Checking product: {product['name']}")
        
        keywords = product['keywords'][0] if product['keywords'] else product['name']
        html, status = await scraper.search(keywords)
        
        if status == 200:
            listings = parse_listings(html)
            result_msgs = my_listing_standing(product['my_price'], product['delivery_cost'], listings, product['name']
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

async def start_daemon(channel):
    await channel.send(f"Starting daemon mode - checking every {CHECK_INTERVAL} seconds. Press Ctrl+C to stop.")
    
    while True:
        try:
            messages = await start_scraper_once()
            result_block = "\n".join(messages)

            for i in range(0, len(result_block), 1900):
                chunk = result_block[i:i+1900]
                await channel.send(f"\n{chunk}\n")

            await asyncio.sleep(CHECK_INTERVAL)
        except Exception as e:
            await channel.send(f"Error in daemon: {e}. Retrying in 60 seconds...")
            await asyncio.sleep(60)
  


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id != RUN_CHANNEL_ID:
        return

    if message.content.lower().startswith('!check'):
        await message.channel.send('Running price check...')
        messages = await start_scraper_once()
        result_block = "\n".join(messages)

        if len(result_block) <= 1900:
            await message.channel.send(f"\n{result_block}\n")
        else:
            for i in range(0, len(result_block), 1900):
                chunk = result_block[i:i+1900]
                await message.channel.send(f"\n{chunk}\n")

        await message.channel.send('\nPrice check complete!')

    if message.content.lower().startswith('!daemon'):
        asyncio.create_task(start_daemon(message.channel))
        await message.channel.send("Daemon started in the background!")
    
    if message.content.lower().startswith('!help'):
        help_text = (
        "**Ebay Monitor Bot Commands**\n\n"
        "`!check`  – Run a one-time price check on all enabled products.\n"
        "`!daemon` – Start continuous monitoring (checks every "
        f"{CHECK_INTERVAL} seconds) in this channel.\n"
        "`!help`   – Show this help message.\n" 
        )   
        await message.channel.send(help_text)
   
         


def main():
    client.run(DISCORD_BOT_TOKEN)