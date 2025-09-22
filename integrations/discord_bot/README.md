# Discord Bot Setup Guide

Run the eBay Price Monitor from Discord and receive results directly in your server.

## ✅ What You Get
- Run checks with `!check`
- Start background monitoring with `!daemon`
- Results posted in your chosen channel
- Uses the same product config in `monitor/config.py`

## Prerequisites
- A Discord account and a server where you can add bots
- Python and project dependencies installed (`pip install -r requirements.txt`)

## 1) Create a Discord Bot and Get the Token
1. Go to the Discord Developer Portal: `https://discord.com/developers/applications`
2. New Application → Name it → Create
3. In the left sidebar, go to Bot → Add Bot
4. Copy the Token → keep it secret (you will put it in `.env`)
5. Under Bot → Privileged Gateway Intents, enable:
   - Message Content Intent (required for reading commands)

## 2) Invite the Bot to Your Server
1. In the app page, go to OAuth2 → URL Generator
2. Scopes: check `bot`
3. Bot Permissions: check at least `Send Messages` and `Read Messages/View Channels`
4. Copy the generated URL and open it to invite the bot to your server

## 3) Configure the Project
1. Create a `.env` file in the project root with your token:
```bash
DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
```
2. Set the channel where the bot will listen for commands. Open `monitor/config.py` and set:
```python
RUN_CHANNEL_ID = 123456789012345678  # Replace with your channel ID
# (Optional) LOG_CHANNEL_ID = 123456789012345678
```
How to get the Channel ID:
- Discord → User Settings → Advanced → Enable Developer Mode
- Right-click the target channel → Copy ID

## 4) Run the Bot
From the project root:
```bash
python run_bot.py
```
You should see a login message in the console.

## 5) Commands
- `!check` — Runs a one-time check for all enabled products and posts results
- `!daemon` — Starts continuous monitoring at `CHECK_INTERVAL` seconds (set in `monitor/config.py`)
  - Stop the daemon with `Ctrl+C` in the terminal running the bot

### Flags
- `-p` or `product`: Product name (supports multi-word names)
- `-price` or `price`: Your price to compare against
- `-del`, `delivery`, or `delievery`: Delivery cost
- `-i` or `-interval`: Interval in seconds (for `!daemon`)

### Examples
- `!check -p retimax 1500 -price 6.95 -del 0`
- `!daemon -p retimax 1500 -price 6.95 -del 0 -i 1800`

## Configuration Notes
- Products are defined in `monitor/config.py` (`PRODUCTS` array)
- Check frequency is `CHECK_INTERVAL` in `monitor/config.py`
- The bot only responds in the channel matching `RUN_CHANNEL_ID`

## Troubleshooting
- If the bot ignores commands:
  - Verify `RUN_CHANNEL_ID`
  - Ensure Message Content Intent is enabled
  - Confirm the bot has permission to read/send messages in the channel
- If you get errors on startup:
  - Ensure `DISCORD_BOT_TOKEN` is correct in `.env`
  - Reinstall dependencies with `pip install -r requirements.txt`

## Security
- Never commit your token to version control
- Rotate the token immediately if leaked
