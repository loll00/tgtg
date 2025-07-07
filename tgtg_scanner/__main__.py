import os
import time
import requests
from tgtg import TgtgClient

# Telegram-Konfiguration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7667257877:AAGTzmC5d4yjyyjCflJPOWWU1rTNNpEaRkw")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1250679325")

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Fehler beim Senden der Telegram-Nachricht: {e}")

# TGTG-Konfiguration
EMAIL = os.getenv("yuliyan.dimitrov08@icloud.com")
PASSWORD = os.getenv("Yuliyan08")
COUNTRY_CODE = os.getenv("49", "49")

client = TgtgClient(email=EMAIL, password=PASSWORD, country_code=COUNTRY_CODE)
seen_item_ids = set()

def check_items():
    try:
        items = client.get_items()
    except Exception as e:
        print(f"Fehler beim Abrufen der TGTG-Daten: {e}")
        return

    for item in items:
        item_id = item.get("item", {}).get("item_id")
        if item_id in seen_item_ids:
            continue

        seen_item_ids.add(item_id)

        title = item.get("display_name", "Unbekannt")
        price = item.get("item", {}).get("price_including_taxes", {}).get("minor_units", 0) / 100
        pickup = item.get("pickup_interval", {}).get("start")
        message = f"📦 <b>TooGoodToGo Alarm!</b>\n🏪 {title}\n💰 {price:.2f} €\n⏰ Abholung: {pickup}"

        print(f"Sende Nachricht für: {title}")
        send_telegram(message)

# Haupt-Loop
if __name__ == "__main__":
    print("TGTG Bot gestartet...")
    while True:
        check_items()
        time.sleep(300)  # alle 5 Minuten prüfen
