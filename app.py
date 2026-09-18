import cloudscraper
from bs4 import BeautifulSoup
import time
import re
import random

# --- CONFIGURATION ---
CHECK_INTERVAL = 60 

TRACK_LIST = [
    {
        "name": "Nike Vomero 5 Women's",
        "url": "https://www.nike.com/t/zoom-vomero-5-womens-shoes-with-reflective-accents-81TPKW/FD0884-025",
        "target": 160.00,
        "tag": "span", "attrs": {"data-testid": "currentPrice-container"} 
    },
    {
        "name": "Nike Patriots Fan Shirt",
        "url": "https://www.nike.com/t/new-england-patriots-2026-afc-champions-roster-mens-t-shirt-ix0xXibu/NP9906FF8K-M23",
        "target": 35.00,
        "tag": "div", "attrs": {"id": "price-container"}
    },
    {
        "name": "H&M",
        "url": "https://www2.hm.com/en_us/productpage.1329140003.html",
        "target": 35.00,
        "tag": "div", "attrs": {"class": "c7e351 a48707"}
    },
]

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})

def check_prices():
    for item in TRACK_LIST:
        try:
            print(f"Checking {item['name']}...")
            response = scraper.get(item['url'], timeout=20)
            
            # 1. Try the standard way (BeautifulSoup)
            soup = BeautifulSoup(response.content, "html.parser")
            price_element = soup.find(item['tag'], attrs=item['attrs'])
            current_price = None

            if price_element:
                text = price_element.get_text(strip=True).replace(",", ".")
                match = re.search(r"(\d+\.\d+|\d+)", text)
                if match:
                    current_price = float(match.group(1))

            # 2. Handle the Result
            if current_price is not None:
                if current_price <= item['target']:
                    print(f"   ✅ ALERT: {item['name']} is ${current_price}!")
                else:
                    print(f"   ❌ Current: ${current_price} (Target: ${item['target']})")
            else:
                print(f"   ⚠️ Still no price found. The site is fully hiding it from bots.")
                
        except Exception as e:
            print(f"   Error: {e}")
        
        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    while True:
        check_prices()
        print(f"\nWaiting {CHECK_INTERVAL}s...\n")
        time.sleep(CHECK_INTERVAL)