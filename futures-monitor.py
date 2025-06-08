from fubon_neo.sdk import FubonSDK, Mode
from dotenv import load_dotenv
import os, json, time
from collections import deque
import requests
import traceback
from datetime import timedelta, datetime

# ─── Load .env ───
env_file = r"D:\Fubon auto venv\555\future_monitor.env"  # Modify as needed
load_dotenv(dotenv_path=env_file.strip())

ACCOUNT          = os.getenv("ACCOUNT")
PASSWORD         = os.getenv("PASSWORD")
CERT_PATH        = os.getenv("CERT_PATH")
CERT_PASSWORD    = os.getenv("CERT_PASSWORD")
TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SYMBOL           = os.getenv("SYMBOL")

# ─── Telegram Notification ───
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"❗ First Telegram send failed: {e}")
        try:
            time.sleep(2)
            requests.post(url, json=payload, timeout=10)
            print("✅ Retry Telegram send successful")
        except Exception as e2:
            print(f"❗ Second Telegram send failed: {e2}")

# ─── Init Fubon SDK ───
sdk = FubonSDK(168, 4)
res = sdk.login(ACCOUNT, PASSWORD, CERT_PATH, CERT_PASSWORD)
if not res.is_success:
    print("❌ Login failed:", res.message)
    exit(1)
sdk.init_realtime(Mode.Normal)

bars = deque(maxlen=60)
last_candle_ts = None
last_trend = None
last_trend_check_time = None
last_check_time = None
last_ma5 = None
subscribed = False
current_minute_data = None

# ─── Safe Reconnect ───
def safe_reconnect():
    global subscribed
    try:
        futopt.disconnect()
    except Exception as e:
        print(f"❗ Failed to disconnect old session: {e}")
    time.sleep(2)
    try:
        futopt.connect()
        print("✅ Reconnected successfully!")
        subscribed = False
    except Exception as e:
        print(f"❌ Reconnect failed: {e}")

# ─── Event Handlers ───
def handle_connect():
    print("✅ Market data connected")

def handle_disconnect(code, message):
    print(f"⚠️ Disconnected: {code}, {message}, retrying...")
    safe_reconnect()

def handle_error(error, tb_info=None):
    print(f"❗ WebSocket error: {error}")
    if tb_info:
        print(tb_info)

# ─── Message Handler ───
def handle_message(msg):
    global last_candle_ts, subscribed, last_trend, last_trend_check_time, last_check_time, last_ma5, current_minute_data

    try:
        obj = json.loads(msg)
        ev = obj.get("event")
        ch = obj.get("channel")

        if ev == "authenticated" and not subscribed:
            print("🔗 Authenticated, subscribing to 1m candles")
            futopt.subscribe({"channel": "candles", "symbol": SYMBOL, "interval": "1m"})
            futopt.subscribe({"channel": "candles", "symbol": SYMBOL, "interval": "1m", "afterHours": True})
            subscribed = True
            return

        if ev == "data" and ch == "candles":
            d = obj["data"]
            ts = d["date"]
            close = d["close"]
            high = d.get("high", close)
            low = d.get("low", close)
            volume = d.get("volume", 0)

            if volume == 0:
                print(f"⚠️ Volume is 0: {ts}")

            minute_ts = ts[:19]

            if current_minute_data is None or minute_ts == current_minute_data["minute_ts"]:
                current_minute_data = {
                    "minute_ts": minute_ts,
                    "close": close,
                    "high": high,
                    "low": low,
                    "volume": volume
                }
                return

            prev_minute_data = current_minute_data
            dt = datetime.strptime(prev_minute_data["minute_ts"], '%Y-%m-%dT%H:%M:%S') + timedelta(seconds=59.999)
            end_ts = dt.strftime('%Y-%m-%dT%H:%M:%S.999+08:00')

            bars.append({
                "date": end_ts,
                "close": prev_minute_data["close"],
                "high": prev_minute_data["high"],
                "low": prev_minute_data["low"],
                "volume": prev_minute_data["volume"]
            })

            print(f"[1mK] {end_ts} Close {prev_minute_data['close']} Volume {prev_minute_data['volume']}")

            current_minute_data = {
                "minute_ts": minute_ts,
                "close": close,
                "high": high,
                "low": low,
                "volume": volume
            }
            last_candle_ts = minute_ts

            if len(bars) < 5:
                return

            closes = [b["close"] for b in bars]
            ma5 = sum(closes[-5:]) / 5 if len(closes) >= 5 else None
            if ma5 is None:
                return

            current_bar = bars[-1]
            previous_bar = bars[-2]

            if last_trend is None or (current_bar["close"] > ma5 and last_trend != 'above'):
                send_telegram(f"[Breakout] {current_bar['date']}\nClose: {current_bar['close']}\n5MA: {round(ma5)}\n→ Close breaks above 5MA")
                last_trend = 'above'
            elif current_bar["close"] < ma5 and last_trend != 'below':
                send_telegram(f"[Breakdown] {current_bar['date']}\nClose: {current_bar['close']}\n5MA: {round(ma5)}\n→ Close falls below 5MA")
                last_trend = 'below'

            if last_trend == 'above' and current_bar["close"] >= ma5 + 9:
                send_telegram(f"[Uptrend Continues] {current_bar['date']}\nClose: {current_bar['close']}\n5MA: {round(ma5)}")
            elif last_trend == 'below' and current_bar["close"] <= ma5 - 9:
                send_telegram(f"[Downtrend Continues] {current_bar['date']}\nClose: {current_bar['close']}\n5MA: {round(ma5)}")

            if (current_bar["high"] - current_bar["low"]) >= 26:
                send_telegram(f"[Volatility Alert] {current_bar['date']}\nHigh: {current_bar['high']} Low: {current_bar['low']}\n→ Range: {current_bar['high'] - current_bar['low']} pts")

            prev_close = previous_bar["close"]
            gap = current_bar["close"] - prev_close
            if gap >= 14:
                t1 = previous_bar["date"].split("T")[1].split("+")[0]
                t2 = current_bar["date"].split("T")[1].split("+")[0]
                send_telegram(f"[Surge] {t1} → {t2}\n{prev_close} → {current_bar['close']} (+{gap})")
            if gap <= -14:
                t1 = previous_bar["date"].split("T")[1].split("+")[0]
                t2 = current_bar["date"].split("T")[1].split("+")[0]
                send_telegram(f"[Drop] {t1} → {t2}\n{prev_close} → {current_bar['close']} ({gap})")

            current_volume = current_bar["volume"]
            prev_volume = previous_bar["volume"]
            volumes = [b["volume"] for b in bars][-5:-1]
            avg_volume = sum(volumes) / len(volumes) if volumes else 0

            print(f"[Volume Check] Current: {current_volume}, Prev: {prev_volume}, 5min Avg: {round(avg_volume)}")

            if (current_volume > prev_volume * 1.5 or current_volume > avg_volume * 1.6) and \
               current_volume > 0 and prev_volume > 0 and avg_volume > 0:
                reason = []
                if current_volume > prev_volume * 1.5:
                    reason.append(f">1.5x last min (x{round(current_volume / prev_volume, 2)})")
                if current_volume > avg_volume * 1.6:
                    reason.append(f">1.6x 5min avg (x{round(current_volume / avg_volume, 2)})")
                send_telegram(
                    f"[Volume Spike] {current_bar['date']}\n"
                    f"Current: {current_volume}, Prev: {prev_volume}, Avg: {round(avg_volume)}\n"
                    f"→ {' & '.join(reason)}"
                )

            if last_check_time is None or (time.time() - last_check_time) >= 333:
                last_check_time = time.time()
                ma5_diff = current_bar["close"] - ma5
                if last_ma5 is not None:
                    ma5_change = ma5 - last_ma5
                    send_telegram(
                        f"[Interval Report] {current_bar['date']}\n"
                        f"Close: {current_bar['close']}, 5MA: {round(ma5)}\n"
                        f"Diff: {round(ma5_diff)} pts\n"
                        f"5MA Δ: {round(ma5_change)} pts"
                    )
                else:
                    send_telegram(
                        f"[Interval Report] {current_bar['date']}\n"
                        f"Close: {current_bar['close']}, 5MA: {round(ma5)}\n"
                        f"Diff: {round(ma5_diff)} pts\n"
                        f"5MA Δ: N/A"
                    )
                last_ma5 = ma5

    except Exception as e:
        print(f"❗ Message handling error: {e}")
        traceback.print_exc()

# ─── Event Callback ───
def on_event(code, content):
    print("=== Event ===")
    print(code)
    print(content)
    if code == "300":
        print("Reconnect triggered")
        send_telegram(f"[Reconnect] Disconnection detected: {content}")
        try:
            accounts = sdk.login(ACCOUNT, PASSWORD, CERT_PATH, CERT_PASSWORD)
            print("Reconnect success")
            send_telegram("[Reconnect] Reconnected successfully")
        except Exception as e:
            print("Reconnect failed")
            print(e)
            send_telegram(f"[Reconnect] Failed: {str(e)}")
    print("=============")

# ─── WebSocket Setup ───
futopt = sdk.marketdata.websocket_client.futopt
futopt.on("connect", handle_connect)
futopt.on("disconnect", handle_disconnect)
futopt.on("error", handle_error)
futopt.on("message", handle_message)
sdk.set_on_event(on_event)

# ─── Start ───
futopt.connect()
print("▶ Connecting...")
while True:
    time.sleep(1)
