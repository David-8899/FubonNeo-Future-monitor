# Fubon Future Monitor

A real-time monitoring script for Taiwan futures (1-minute K-lines) using the Fubon SDK and Telegram notifications.

It detects breakout/breakdown based on 5MA and alerts volume spikes, surges, and volatility patterns — perfect for short-term day trading analysis or strategy prototyping.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

📌 Features

- ✅ Real-time 1-minute candle data via Fubon SDK WebSocket
- ✅ Detects 5MA breakout / breakdown and trend continuation
- ✅ Alerts high volatility bars and sudden price surges/drops
- ✅ Detects volume spike patterns using recent average and last bar
- ✅ Sends all signals via Telegram, with retry on failure
- ✅ Auto reconnects on disconnection

---

📈 Strategy Logic

- **Breakout/Breakdown**: Close price crosses above or below 5MA
- **Trend Continuation**: Close exceeds 5MA by 9+ pts (above or below)
- **Volatility Alert**: If candle range ≥ 26 pts
- **Surge/Drop**: If 1-minute close-to-close gap ≥ ±14 pts
- **Volume Spike**: If current volume > 1.5× previous OR > 1.6× 5min avg
- **Interval Summary**: Every ~5 mins, reports 5MA delta and close diff

---

🛠️ Installation
Clone the repo or download as .zip

git clone https://github.com/yourname/fubon-future-monitor.git
cd fubon-future-monitor

Create your .env file

cp .env.example .env

Install required packages

pip install -r requirements.txt

Run the monitor

python future-monitor.py

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

📎 Requirements
Python 3.8+

Fubon SDK (external)

pip packages:

requests

python-dotenv

⚠️ Disclaimer
This tool is for educational use only.
Use it at your own risk.
This is not a trading recommendation system.

📄 License
MIT © 2025 David Lee
