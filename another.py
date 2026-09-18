import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import random
import sys
from mailer import send_email

# In Selenium, we use CSS Selectors because they are faster.
# To find an ID, use # (e.g., #price-container).
# To find a Class, use . (e.g., .price-amount).
# To find a Data Test ID, use brackets (e.g., [data-testid="value"]).
# To find selector, go to inspect and find where price is then do copy > copy selector

# --- CONFIGURATION ---
CHECK_INTERVAL = 18000

TRACK_LIST = [
    {
        "name": "Nike Vomero 5 Women's",
        "url": "https://www.nike.com/t/zoom-vomero-5-womens-shoes-with-reflective-accents-81TPKW/FD0884-025",
        "target": 160.00,
        "selector": '#price-container' # CSS Selector
    },
    {
        "name": "Zara STRIPED JACQUARD SHIRT",
        "url": "https://www.zara.com/us/en/striped-jacquard-shirt-p09144304.html?v1=454900532&v2=2215137",
        "target": 20.00,
        "selector": '#main > div > div.product-detail-view-std > div.product-detail-view__main-content > div.product-detail-view__main-info > div > div.product-detail-info__info > div.product-detail-info__price > div > span > ins > span.price-current__amount > div > span'
    },
    {
        "name": "Nike Patriots Shirt",
        "url": "https://www.nike.com/t/new-england-patriots-2026-afc-champions-roster-mens-t-shirt-ix0xXibu/NP9906FF8K-M23",
        "target": 35.00,
        "selector": '#price-container' 
    },
    {
        "name": "H&M Relaxed-Fit Short-Sleeved Utility Shirt",
        "url": "https://www2.hm.com/en_us/productpage.1293696001.html",
        "target": 35.00,
        "selector": '#main-content > div.rOGz > div > div > div:nth-child(2) > div > div > div.c7e351.a48707 > span.c7cac7.f3d1ea.d2184c.bdde6d'
    },
]

def get_driver():
    try:
        options = uc.ChromeOptions()
        # options.add_argument('--headless') # Uncomment this to hide the browser window
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox') # Required for Linux servers
        options.add_argument('--disable-dev-shm-usage')
        driver = uc.Chrome(options=options, version_main=144)
        return driver
    except:
        print(" ⚠️ Update Chrome to version 144!")
        sys.exit(1)

def clean_price(text):
    # Extracts number from strings like "$170.00" or "Current Price: $34.99"
    match = re.search(r"(\d+\.\d+|\d+)", text.replace(",", "."))
    return float(match.group(1)) if match else None

def check_prices():
    driver = get_driver()
    report = [] 
    
    print(f"\n--- Starting Price Check: {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    try:
        for item in TRACK_LIST:
            msg = ""
            try:
                driver.get(item['url'])
                # Slower wait to ensure JS loads the price
                time.sleep(10) 
                wait = WebDriverWait(driver, 20)
                price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, item['selector'])))
                
                price_text = price_element.text
                current_price = clean_price(price_text)
                
                if current_price:
                    status = f"{item['name']}: ${current_price}"
                    if current_price <= item['target']:
                        msg = f"✅ ALERT: {status} (Target reached!)"
                    else:
                        msg = f"❌ Above Target: {status} (Target: ${item['target']})"
                else:
                    msg = f"⚠️ Error: Could not parse price for {item['name']}"
            except Exception as e:
                msg = f"⚠️ Timeout/Blocked: {item['name']}"
            
            print(f"   {msg}") 
            report.append(msg)
            time.sleep(random.randint(5, 10))
            
    finally:
        # This ensures the browser closes and email sends even if there's an error
        driver.quit()
        if report:
            full_report = "\n".join(report)
            print("\n--- Sending Email Report ---")
            send_email(full_report)

if __name__ == "__main__":
    while True:
        check_prices()
        hours = CHECK_INTERVAL/60/60
        print(f"\nWaiting {int(hours)}hrs before next cycle...\n")
        time.sleep(CHECK_INTERVAL)
        
        