# eBay Price Monitor

A Python-based price monitoring tool that automatically tracks eBay listings for your products and alerts you when competitors are selling cheaper.

## **What It Does**

- **Automatically searches** eBay for your products
- **Monitors competitor prices** in real-time
- **Desktop notifications** when someone undercuts you
- **Logs all activity** for tracking and analysis


## **Features**

- **Smart HTML parsing** - Adapts to eBay's changing structure
- **Competitor analysis** - Identifies listings cheaper than yours
- **Desktop alerts** - Instant notifications when competition is found
- **Comprehensive logging** - Track all monitoring activity
- **Configurable settings** - Easy to modify products and prices

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
git clone https://github.com/Igor-Kaminski/Scraper/tree/main
cd ebay-price-monitor
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

### **4. Configure your settings**
Edit `config.py` with your product details and notification preferences:
```python
PRODUCT_KEYWORDS = ['your product name']
MY_BASE_PRICE = <your price>
MY_DELIEVERY_COST = <your delievery cost>

# Notification settings
NOTIFICATION_TITLE = '🚨 Price Alert!'
NOTIFICATION_MESSAGE = '{count} competitors cheaper than you!'
NOTIFICATION_TIMEOUT = 10
```

## 🎮 **Usage**

### **Basic Usage**
```bash
python main.py
```

### **What Happens**
1. **Searches eBay** for your configured products
2. **Parses all listings** and extracts prices
3. **Compares to your price** and identifies cheaper competitors
4. **Shows desktop notification** if competition is found
5. **Logs everything** to `logs/scraper.log`

## ⏱️ **Automation**

### **Linux / macOS**
Use `cron` to run the scraper automatically:

```bash
crontab -e
# Add the following line to run every hour
0 * * * * /full/path/to/.venv/bin/python /full/path/to/main.py >> /full/path/to/logs/cron.log 2>&1
```

### **Windows**
Use Task Scheduler to run main.py every hour:

1. Open **Task Scheduler** → **Create Task**
2. Set **Trigger** → **Daily** → **Repeat task every 1 hour**
3. Set **Action** → **Start a program** → **Program**: `python.exe`, **Arguments**: `main.py`

**Notes:**
- Replace `/full/path/to/` with the absolute path to your project and virtual environment
- `>> cron.log 2>&1` ensures all output and errors are logged
- Cron runs your script even if the terminal is closed
- The task runs even if your PC is locked
- Make sure the paths use full absolute paths




## 📁 **Project Structure**

```
ebay-price-monitor/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── scraper.py           # eBay scraping logic
├── analyser.py          # Price analysis and notifications
├── requirements.txt     # Python dependencies
├── logs/                # Activity logs
└── README.md            # README
```

## ⚙️ **Configuration**

### **Product Settings**
- `PRODUCT_KEYWORDS`: List of search terms for your products
- `MY_BASE_PRICE`: Your selling price
- `MY_DELIEVERY_COST`: Your shipping cost

### **Notification Settings**
- `NOTIFICATION_TITLE`: Title of the desktop alert
- `NOTIFICATION_MESSAGE`: Message text (use `{count}` for number of cheaper listings)
- `NOTIFICATION_TIMEOUT`: How long the notification stays visible (in seconds)


## 🔧 **Customization**

### **Add New Products**
```python
# In config.py
PRODUCT_KEYWORDS = ['product 1', 'product 2', 'product 3']
```

### **Change Price Thresholds**
```python
# In config.py
MY_BASE_PRICE = 25.99
MY_DELIEVERY_COST = 5.99
```

### **Modify Notification Settings**
```python
# In config.py, customize your notification preferences
NOTIFICATION_TITLE = '🚨 Price Alert!'
NOTIFICATION_MESSAGE = '{count} competitors cheaper than you!'
NOTIFICATION_TIMEOUT = 10  # Show for 10 seconds

# Examples:
NOTIFICATION_TITLE = 'Competition Alert!'
NOTIFICATION_MESSAGE = 'Found {count} cheaper listings!'
NOTIFICATION_TIMEOUT = 15  # Show for 15 seconds
```

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



