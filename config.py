'''
CONFIG SETTINGS
'''

PRODUCT_KEYWORDS = ['retimax 1500']  # Product to monitor - only one product can be monitored at a time
MY_BASE_PRICE = 100            
MY_DELIEVERY_COST = 0  # Set to 0 if you offer free shipping, otherwise add your shipping cost

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
    "authority": "www.ebay.co.uk",
    "method": "GET",
    "path": "/sch/i.html?_nkw=retimax+1500&_sacat=0&_from=R40&_trksid=m570.l1313&_odkw=retimax+1500%5C&_osacat=0",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "referer": "https://www.ebay.co.uk/sch/i.html?_nkw=retimax+1500%5C&_sacat=0&_from=R40&_trksid=m570.l1313&_odkw=retimax+1500&_osacat=0",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-full-version": "\"139.0.7258.127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-ch-ua-platform-version": "\"6.16.1\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.3"
}