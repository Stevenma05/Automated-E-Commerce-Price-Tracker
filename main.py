import requests
from bs4 import BeautifulSoup
import time

# --- CONFIGURATION ---
URL = "https://www.nike.com/t/zoom-vomero-5-womens-shoes-with-reflective-accents-81TPKW/FD0884-025" # Replace with your URL
TARGET_PRICE = 180.00  # The price you're waiting for
CHECK_INTERVAL = 10  # 1 minute in seconds
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def check_price():
    try:
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        # NOTE: You must inspect the webpage and find the correct CSS selector
        # Example: <span id="priceblock_ourprice">$199.99</span>
        price_text = soup.find(id="price-container").get_text()
        
        # Clean the string (remove $ and commas) and convert to float
        current_price = float(price_text.replace("$", "").replace(",", "").strip())

        if current_price <= TARGET_PRICE:
            send_notification(current_price)
            return True # Stop the script once it finds the deal
        else:
            print(f"Still ${current_price}. Checking again in an hour...")
            return False

    except Exception as e:
        print(f"Error checking site: {e}")
        return False

def send_notification(price):
    # This is where you'd plug in a Discord Webhook or Twilio API
    print(f"--- ALERT! PRICE DROPPED TO ${price} ---")
    # Example for Discord: requests.post(WEBHOOK_URL, data={"content": f"Buy now! ${price}"})

if __name__ == "__main__":
    found = False
    while not found:
        found = check_price()
        if not found:
            time.sleep(CHECK_INTERVAL)