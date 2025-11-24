import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# --- 1. FIX TURKISH CHARACTERS ---
# This forces your terminal to use UTF-8 so 'İzmir' prints correctly
sys.stdout.reconfigure(encoding='utf-8')

# --- 2. SETUP BROWSER ---
print("Starting the browser...")
options = webdriver.ChromeOptions()
# We pretend to be a real user to avoid getting blocked
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- 3. CONFIGURATION ---
base_url = "https://www.hepsiemlak.com/izmir-satilik"
total_pages_to_scrape = 75
all_data = []

# --- 4. THE MAIN LOOP ---
current_page = 45

try:
    print(f"Targeting: {base_url}")
    
    while current_page <= total_pages_to_scrape:
        print(f"\n--- Processing Page {current_page} ---")
        
        # Navigate to the specific page number
        # Trick: We just add ?page=1, ?page=2 to the URL
        url_to_visit = f"{base_url}?page={current_page}"
        driver.get(url_to_visit)
        
        # Wait for data to load (crucial!)
        time.sleep(5)
        
        # Parse the HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")
        listings = soup.find_all("li", class_="listing-item")
        print(f"Found {len(listings)} ads.")
        
        for house in listings:
            try:
                # EXTRACT PRICE
                # .strip() removes the big empty spaces you saw earlier
                price_raw = house.find("span", class_="list-view-price").text.strip()
                # Turn "7.500.000 TL" into "7500000"
                price_clean = price_raw.replace("TL", "").replace(".", "").strip()
                
                # EXTRACT LOCATION
                location = house.find("span", class_="list-view-location").text.strip()
                
                # EXTRACT DETAILS (Rooms, m2, Age)
                # These are often in a list, so we grab them all and search text
                details_text = [span.text.strip() for span in house.find_all("span", class_="celly")]
                
                rooms = "Unknown"
                m2 = "Unknown"
                age = "Unknown"
                
                for item in details_text:
                    if "m²" in item:
                        m2 = item.replace("m²", "").strip()
                    elif "Yaşında" in item or "Sıfır Bina" in item:
                        age = item
                    elif "+" in item or "Stüdyo" in item:
                        rooms = item

                # Add to our data list
                all_data.append({
                    "District": location,
                    "Price": price_clean,
                    "Rooms": rooms,
                    "Size_m2": m2,
                    "Age": age
                })
                
            except AttributeError:
                continue # If one ad is broken, skip it and keep going

        current_page += 1

finally:
    # --- 5. SAVE THE DATA ---
    driver.quit()
    print("\nBrowser closed.")
    
    if len(all_data) > 0:
        df = pd.DataFrame(all_data)
        # Save as Excel
        df.to_excel("izmir_houses_part2.xlsx", index=False, )
        print(f"SUCCESS! Saved {len(all_data)} listings to 'izmir_houses_part2.xlsx'")
        print("Check your folder for the file!")
    else:
        print("No data found. Something went wrong.")