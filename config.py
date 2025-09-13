'''
CONFIG SETTINGS
'''

# Multiple product support
PRODUCTS = [
    {
        'name': 'rtx 3070', # Will appear in the logs file and notifications
        'keywords': ['rtx 3070'], # Actual search term used in eBay search
        'my_price': 200,
        'delivery_cost': 0,
        'enabled': True # Whether to search for this product, set to False to skip
    },
    # Example of how to add more products:
    # {
    #     'name': 'iPhone 15',
    #     'keywords': ['iPhone 15', 'iPhone 15 Pro'],
    #     'my_price': 800,
    #     'delivery_cost': 10,
    #     'enabled': True
    # },
    # {
    #     'name': 'Gaming Laptop',
    #     'keywords': ['gaming laptop', 'gaming notebook'],
    #     'my_price': 1200,
    #     'delivery_cost': 0,
    #     'enabled': False  # This product is disabled
    # }
]


# Scheduler settings
SCHEDULER = False  # False = run once and exit, True = run as background daemon
CHECK_INTERVAL = 3600  # How often to check prices (seconds) 

# Notification settings
NOTIFICATION_TITLE = '🚨 Price Alert!'
NOTIFICATION_MESSAGE = '{count} competitors cheaper than you!' # Message text, use {count} to show number of cheaper competitors found
NOTIFICATION_TIMEOUT = 10 # How long the notification stays visible on screen (seconds)

# =============================================================================
# HTTP HEADERS - these worked well for me
# =============================================================================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}