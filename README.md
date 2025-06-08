# Fubon Futures Monitor

A real-time futures monitoring script for the Taiwan market using the Fubon SDK and Telegram notifications.  
Designed for traders and analysts to detect key breakout, surge, and volume spike conditions based on 1-minute candles.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📌 Features

- ✅ Connects to Fubon SDK real-time futures data  
- ✅ Subscribes to 1-minute candles with after-hours support  
- ✅ Detects breakouts/breakdowns based on 5MA logic  
- ✅ Monitors high-low range volatility and price momentum  
- ✅ Sends structured alerts via Telegram with retry logic  
- ✅ Auto reconnect on disconnection events

---

## 📈 Monitoring Logic

- 📊 Breakout if price crosses above 5MA for the first time  
- 📉 Breakdown if price crosses below 5MA for the first time  
- ⬆️ Continued uptrend if close ≥ 5MA + 9  
- ⬇️ Continued downtrend if close ≤ 5MA - 9  
- ⚡ Price surge/drop if 1-min gap ≥ ±14 points  
- 📶 Volume spike if >1.5x last min or >1.6x 5-min avg  
- 🕒 Periodic update every 333s: close vs MA and MA delta

---

## 🛠️ Installation

You can either clone the repo using Git (if available):

```bash
git clone https://github.com/David-8899/FubonNeo-Futures-monitor.git
cd FubonNeo-Futures-monitor
```

Or download the project as a `.zip` file directly from the GitHub page.

Then:

1. Copy `.env.example` and rename it to `.env`  
2. Fill in your Fubon credentials and Telegram bot token  
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the script:

```bash
python futures-monitor.py
```

---

## 📦 Fubon SDK Setup

This project requires the **Fubon SDK (`fubon_neo.sdk`)**, which is **not available on PyPI**.

To run this script:

1. You must have an active trading account with Fubon Securities.  
2. Request access to their Python SDK via your broker or Fubon customer support.  
3. After receiving the SDK package (usually a `.zip` or folder), place it in your working environment and ensure it is importable (e.g., placed alongside `exit_monitor.py` or added to `PYTHONPATH`).

> ❗ This repository **does not include or distribute** the SDK itself due to licensing restrictions.

---

## ⚙️ Environment Variables

See `.env.example` for required fields:

```env
ACCOUNT=your_account
PASSWORD=your_password
CERT_PATH=path/to/your_certificate.pfx
CERT_PASSWORD=your_cert_password

TELEGRAM_TOKEN_1=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## 📎 Requirements

- Python 3.8+
- `requests`, `python-dotenv`
- Fubon SDK (external, see section above)

---

## ⚠️ Disclaimer

This script is for educational and monitoring purposes only.
Use at your own risk. Test thoroughly in non-production environments before applying to real trades.

---

## 📄 License

MIT © 2025 David Lee
