📈 TW Futures Price Monitor
A real-time futures price monitoring script for the Taiwan market using the Fubon Securities SDK.
This script analyzes 1-minute candle data and sends trading alerts to Telegram based on price movements, volatility, and volume anomalies.

🔧 Features
Telegram Alerts
Automatically sends real-time alerts when:

Price crosses above or below 5MA

Trend continues with price > MA ±9 points

High-low range exceeds 26 points (volatility spike)

Close-to-close price change ≥ ±14 points (momentum alert)

Volume spikes compared to previous minute or 5-min average

Periodic report every 333 seconds showing price–MA divergence

Auto Reconnect Handling
Handles SDK or WebSocket disconnections and attempts automatic recovery.

Clean Console Output
Prints structured 1-minute candle data and volume insights.

📦 Requirements
Python 3.8 or higher

Fubon Neo SDK (custom SDK, not public)

Telegram Bot token & Chat ID

.env file containing credentials and settings

🚀 Getting Started
Clone this repository

Install dependencies:

pip install -r requirements.txt

Create a .env file using the format below

Run the monitor:

python future-monitor.py

📁 .env Example
ACCOUNT=your_account_id
PASSWORD=your_password
CERT_PATH=D:/your_cert_file.pfx
CERT_PASSWORD=your_cert_password
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
SYMBOL=MXF

🧠 Strategy Logic
This script tracks real-time market signals using the following logic:

5MA Breakout Detection: Detects first time price crosses above or below 5-minute MA

Trend Continuation: Detects sustained move when price exceeds MA ±9 points

Volatility Alerts: Alerts when candle’s high-low range ≥ 26 points

Momentum Shifts: Detects strong 1-minute price moves ≥ 14 points

Volume Spikes: Compares current volume to previous and 5-min average

333-second Interval Reports: Periodic summary of price–MA gap and MA change

All timestamps in Telegram are formatted using Taiwan local time (UTC+8)

📎 License
This project is licensed under the MIT License.

🙋 About
This is a side project built to assist with real-time futures market monitoring.
Currently supports tracking one symbol at a time.
Developed by David-8899 using the Fubon Neo SDK and Telegram API.

Feel free to fork, customize, or suggest improvements via GitHub issues.
