# eBay Price Monitor

A Python-based price monitoring tool that automatically tracks eBay listings for your products and alerts you when competitors are selling cheaper.

## **What It Does**

- **Automatically searches** eBay for your products
- **Monitors competitor prices** in real-time
- **Desktop notifications** when someone undercuts you
- **Logs all activity** for tracking and analysis
- **Runs as daemon** - continuous background monitoring (optional)


## **Features**

- **Multi-product support** - Monitor multiple products simultaneously
- **Smart HTML parsing** - Adapts to eBay's changing structure
- **Competitor analysis** - Identifies listings cheaper than yours
- **Desktop alerts** - Instant notifications when competition is found
- **Comprehensive logging** - Track all monitoring activity
- **Links log** - Full URLs saved to `logs/scraper_links.log`
- **Configurable settings** - Easy to modify products and prices
- **Built-in daemon mode** - Run continuously in background
- **Flexible scheduling** - Choose between one-time or continuous monitoring
- **Discord bot integration (optional)** - Run checks from Discord and post results in a channel


## **Requirements**

- Python 3.7+
- beautifulsoup4==4.13.4
- requests==2.32.4
- plyer==2.1.0 
- lxml==6.0.0 
- fake-useragent==2.2.0
- schedule==1.2.2
- PySocks==1.7.1

## 🛠️ **Installation**

### **1. Clone the repository**
```bash
git clone https://github.com/Igor-Kaminski/Scraper.git
cd Scraper
```

### **2. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or: venv\Scripts\activate  # On Windows
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure your products**
Edit `monitor/config.py` to add your products to monitor:
```python
# Multi-product configuration
PRODUCTS = [
    {
        'name': 'retimax 1500',                    # Display name for notifications and logs
        'keywords': ['retimax 1500'],              # Search terms for eBay
        'my_price': 100,                          # Your selling price
        'delivery_cost': 0,                       # Your delivery cost
        'enabled': True                           # Enable/disable this product
    }
    # Add more products here...
]

# Scheduler settings
SCHEDULER = False  # False = run once, True = run as daemon
CHECK_INTERVAL = 3600  # How often to check (seconds) 

# Notification settings
NOTIFICATION_TITLE = '🚨 Price Alert!'
NOTIFICATION_MESSAGE = '{count} competitors cheaper than you!'
NOTIFICATION_TIMEOUT = 10
```

## 🎮 **Usage**

### **Run Once (Default, async under the hood)**
```bash
python run_scraper.py
```
- Checks prices once and exits
- Perfect for cron jobs or manual runs

### **Run as Daemon (async)**
1. Set `SCHEDULER = True` in `monitor/config.py`
2. Run `python run_scraper.py`
3. Press `Ctrl+C` to stop gracefully

```bash
python run_scraper.py
# Output: Starting async daemon - checking every 3600 seconds
# Press Ctrl+C to stop
```

### **Discord Bot (Optional)**
- You can control the scraper and receive results directly in Discord.
- Quick start: set `DISCORD_BOT_TOKEN` in `.env`, set `RUN_CHANNEL_ID` in `monitor/config.py`, then run:
```bash
python run_bot.py
```
- For full setup and detailed instructions, see the Discord guide: [Discord Bot Setup Guide](integrations/discord_bot/README.md)

### **What Happens**
1. **Checks each enabled product** in your PRODUCTS list
2. **Searches eBay** using the first keyword for each product
3. **Parses all listings** and extracts prices
4. **Compares to your price** and identifies cheaper competitors
5. **Shows product-specific notifications** if competition is found
6. **Logs everything** to `logs/scraper.log`
7. **Saves full links of cheaper listings** to `logs/scraper_links.log`
8. **Repeats asynchronously** every hour (if daemon mode enabled)

## ⏱️ **Automation**

### **Option 1: Built-in Daemon (Recommended)**
Enable the built-in daemon mode for continuous monitoring:

1. Set `SCHEDULER = True` in `monitor/config.py`
2. Run `python run_scraper.py`
3. The daemon runs continuously until stopped with `Ctrl+C`

**Benefits:**
- ✅ **No external setup** - works out of the box
- ✅ **Easy to start/stop** - just run the script
- ✅ **Configurable timing** - adjust `CHECK_INTERVAL` as needed
- ✅ **Graceful shutdown** - handles `Ctrl+C` properly

### **Option 2: External Schedulers**

#### **Linux / macOS (Cron)**
```bash
crontab -e
# Add the following line to run every hour
0 * * * * /full/path/to/.venv/bin/python /full/path/to/run_scraper.py >> /full/path/to/logs/cron.log 2>&1
```

#### **Windows (Task Scheduler)**
1. Open **Task Scheduler** → **Create Task**
2. Set **Trigger** → **Daily** → **Repeat task every 1 hour**
3. Set **Action** → **Start a program** → **Program**: `python.exe`, **Arguments**: `run_scraper.py`

**Notes:**
- Use external schedulers only if you prefer `SCHEDULER = False`
- Replace `/full/path/to/` with the absolute path to your project
- External schedulers work with one-time runs only




## 📁 **Project Structure**

```
Scraper/
├── run_scraper.py         # Entry point for CLI (async run/daemon)
├── run_bot.py             # Entry point for Discord bot (async)
├── bash_scraper.sh        # Bash helper (optional)
├── requirements.txt       # Python dependencies
├── logs/                  # Activity logs and cheaper links
├── monitor/
│   ├── main.py            # Orchestration (async run_once/run_daemon
│   ├── config.py          # Configuration settings
│   ├── scraper.py         # Async eBay scraping logic (aiohttp)
│   └── analyser.py        # HTML parsing and price analysis
├── integrations/
│   └── discord_bot/
│       ├── bot.py         # Discord bot commands (!check, !daemon)
│       └── README.md      # Setup & configuration guide
└── README.md              # This file
```

## ⚙️ **Configuration**

### **Product Settings**
Each product in the `PRODUCTS` array has these settings:
- `name`: Display name shown in notifications and logs
- `keywords`: List of search terms (uses first one for eBay search)
- `my_price`: Your selling price for this product
- `delivery_cost`: Your delivery cost (set to 0 for free shipping)
- `enabled`: `True` to monitor, `False` to skip this product

### **Scheduler Settings**
- `SCHEDULER`: Run mode - `False` for one-time, `True` for daemon
- `CHECK_INTERVAL`: How often to check prices (seconds) 

### **Notification Settings**
- `NOTIFICATION_TITLE`: Title of the desktop alert
- `NOTIFICATION_MESSAGE`: Message text (use `{count}` for number of cheaper listings)
- `NOTIFICATION_TIMEOUT`: How long the notification stays visible (in seconds)

### **Discord (Optional)**
- Set `DISCORD_BOT_TOKEN` in `.env`
- Set `RUN_CHANNEL_ID` (and optionally `LOG_CHANNEL_ID`) in `monitor/config.py`
- Run the bot with `python run_bot.py`
- Full instructions: [Discord Bot Setup Guide](integrations/discord_bot/README.md)

### **Links Logging**
- Full URLs of cheaper listings are written to `logs/scraper_links.log`
- Console output stays clean (no full URLs), only titles and prices



## ⚠️ **Important Notes**

- **Respect eBay's terms of service**
- **Don't make requests too frequently**
- **Use responsibly** 

## 🐛 **Troubleshooting**

### **No listings found?**
- Check if eBay is blocking your requests
- Verify your search keywords
- Check the logs for errors

### **Notifications not working?**
- Ensure `plyer` is installed
- Check your desktop notification settings
- Try running with sudo (Linux permission issues)

### **Getting blocked by eBay?**
- Add delays between requests
- Update your headers
- Consider using the official eBay API

##  **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ **Disclaimer**

This tool is for educational and legitimate business purposes only. Users are responsible for complying with eBay's terms of service and applicable laws. The developers are not responsible for any misuse of this software.



