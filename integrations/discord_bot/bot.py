'''
Discord bot with scraper logic
'''


from monitor import EbayScraper, parse_listings, PRODUCTS, RUN_CHANNEL_ID, LOG_CHANNEL_ID, DISCORD_BOT_TOKEN, CHECK_INTERVAL
import discord
import asyncio

async def start_scraper_once(arguments=None):
    scraper = EbayScraper()
    messages = []

    if arguments is None:
        products_to_check = [p for p in PRODUCTS if p.get('enabled', True)]
    else:
        product_name = arguments.get('product_name', 'Unnamed Product')
        keywords = [arguments.get('product_name')] if arguments.get('product_name') else [product_name]
        my_price = arguments.get('price', 0.0)
        delivery_cost = arguments.get('delivery_price', 0.0)

        products_to_check = [{
            'name': product_name,
            'keywords': keywords,
            'my_price': my_price,
            'delivery_cost': delivery_cost,
            'enabled': True
        }]

    for product in products_to_check:
        messages.append(f"Checking product: {product['name']}")
        
        search_keywords = product['keywords'][0] if product['keywords'] else product['name']
        html, status = await scraper.search(search_keywords)
        
        if status == 200:
            listings = parse_listings(html)
            result_msgs = my_listing_standing(
                product['my_price'], 
                product['delivery_cost'], 
                listings, 
                product['name']
            )
            messages.extend(result_msgs)
        else:
            messages.append(f"Failed to check {product['name']} (status {status})")

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

async def start_daemon(channel, arguments=None):
    interval = CHECK_INTERVAL
    if arguments and arguments.get('interval'):
        interval = float(arguments['interval'])

    await channel.send(f"Starting daemon mode - checking every {interval} seconds. Press Ctrl+C to stop.")

    while True:
        try:
            messages = await start_scraper_once(arguments)
            result_block = "\n".join(messages)

            for i in range(0, len(result_block), 1900):
                chunk = result_block[i:i+1900]
                await channel.send(f"\n{chunk}\n")

            await asyncio.sleep(interval)
        except Exception as e:
            await channel.send(f"Error in daemon: {e}. Retrying in 60 seconds...")
            await asyncio.sleep(60)

def get_arguments(message):
    arguments = {
        'product_name': None,
        'price': None,
        'delivery_price': None
    }

    parts = message.split()
    i = 1  
    while i < len(parts):
        if parts[i] in ['-p', 'product']:
            i += 1
            name_parts = []
            while i < len(parts) and not parts[i].startswith('-'):
                name_parts.append(parts[i])
                i += 1
            arguments['product_name'] = " ".join(name_parts)
        elif parts[i] in ['-price', 'price']:
            if i + 1 < len(parts):
                arguments['price'] = float(parts[i+1])
            i += 2
        elif parts[i] in ['-del', 'del', 'delivery']:
            if i + 1 < len(parts):
                arguments['delivery_price'] = float(parts[i+1])
            i += 2
        elif parts[i] in ['-i', '-interval']:
            if i + 1 < len(parts):
                arguments['interval'] = float(parts[i+1])
            i += 2    
        else:
            i += 1

    return arguments



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
        actual_message = message.content
        await message.channel.send('Running price check...')
        arguments = get_arguments(actual_message)

        if arguments == 0:
            messages = await start_scraper_once()
        else: 
            messages = await start_scraper_once(arguments)
        
        result_block = "\n".join(messages)

        if len(result_block) <= 1900:
            await message.channel.send(f"\n{result_block}\n")
        else:
            for i in range(0, len(result_block), 1900):
                chunk = result_block[i:i+1900]
                await message.channel.send(f"\n{chunk}\n")

        await message.channel.send('\nPrice check complete!')
        
    if message.content.lower().startswith('!daemon'):
        args = get_arguments(message.content) 
        asyncio.create_task(start_daemon(message.channel, arguments=args))
        await message.channel.send("Daemon started in the background!")
    
    
    if message.content.lower().startswith('!help'):
        help_text = f"""**Ebay Monitor Bot Commands**

        `!check`  – Run a one-time price check on all enabled products.
        `!check -p <product> -price <your_price> -del <delivery_cost>` – Run a one-time price check with custom flags.
        `!daemon` – Start continuous monitoring (checks every {CHECK_INTERVAL} seconds) in this channel.
        `!daemon -i <seconds>` – Start daemon with a custom interval between checks
        `!help`   – Show this help message.
        """
        await message.channel.send(help_text)
   
         


def main():
    client.run(DISCORD_BOT_TOKEN)