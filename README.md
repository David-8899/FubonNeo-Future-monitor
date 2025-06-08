Fubon Futures Monitor

A real-time monitoring script for Taiwan futures (1-minute K-lines) using the Fubon SDK and Telegram notifications.
It detects breakout/breakdown based on 5MA and alerts volume spikes, surges, and volatility patterns — perfect for short-term day trading analysis or strategy prototyping.

📌 Features

✅ Real-time 1-minute candle data via Fubon SDK WebSocket

✅ Detects 5MA breakout / breakdown and trend continuation

✅ Alerts high volatility bars and sudden price surges/drops

✅ Detects volume spike patterns using recent average and last bar

✅ Sends all signals via Telegram, with retry on failure

✅ Auto reconnects on disconnection


📈 Strategy Logic

Breakout/Breakdown: Close price crosses above or below 5MA

Trend Continuation: Close exceeds 5MA by 9+ pts (above or below)

Volatility Alert: If candle range ≥ 26 pts

Surge/Drop: If 1-minute close-to-close gap ≥ ±14 pts

Volume Spike: If current volume > 1.5× previous OR > 1.6× 5min avg

Interval Summary: Every ~5 mins, reports 5MA delta and close diff


🛠️ Installation

Clone the repo using git:
git clone https://github.com/yourname/FubonNeo-Futures-monitor.git
cd FubonNeo-Futures-monitor

Or download the project as a .zip file from GitHub and unzip it.

Create your .env file:

cp .env.example .env

Install required packages:
pip install -r requirements.txt

Run the monitor:
python futures-monitor.py


📦 Fubon SDK Setup
This script requires the Fubon SDK (fubon_neo.sdk), which is not available on PyPI.

To use this:

Contact your Fubon broker to obtain access to the SDK.

Place the SDK files in your environment so that import fubon_neo.sdk works.

This repository does not include or distribute the SDK.


⚙️ Environment Variables

Create a .env file like this:

ACCOUNT=your_fubon_account

PASSWORD=your_password

CERT_PATH=path/to/cert.pfx

CERT_PASSWORD=your_cert_password

TELEGRAM_TOKEN=your_bot_token

TELEGRAM_CHAT_ID=your_chat_id

SYMBOL=TXFA1 # or your desired symbol


🧱 File Structure

futures-monitor.py – Main script
.env.example – Environment variable template
requirements.txt – pip package list
README.md – Project description
LICENSE – MIT license
.gitignore – Excluded sensitive files (e.g., .env)


🧠 How It Works

Connects to Fubon SDK WebSocket using your provided symbol

Receives 1-minute candle data, updates moving buffer

Calculates 5MA and compares close price to generate signals

Detects surges, breakdowns, volatility, and volume spikes

Sends formatted alerts to Telegram via Bot API (with retry)


⚠️ Disclaimer

This tool is for educational use only.
Use it at your own risk.
This is not a financial recommendation system.


📄 License

MIT © 2025 David Lee
