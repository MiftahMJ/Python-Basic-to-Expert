# import time
# import random
# import json
# from urllib.parse import quote
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium_stealth import stealth
# import tempfile
#
# # Constants
# PROXY_USERNAME = "yabada_djkVV"
# PROXY_PASSWORD = "yuhimR42_yabada"
# ENDPOINT = "pr.oxylabs.io:7777"
# TARGET_ITEMS = 50  # Set a realistic target number of items to collect per location
#
#
# # Function to set up proxies
# def chrome_proxy(user: str, password: str, endpoint: str) -> dict:
#     wire_options = {
#         "proxy": {
#             "http": f"http://{user}:{password}@{endpoint}",
#             "https": f"https://{user}:{password}@{endpoint}",
#         }
#     }
#     return wire_options
#
#
# # Load existing data to append new results
# def load_existing_data(filepath):
#     try:
#         with open(filepath, 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}
#
#
# # Save the collected data to JSON
# def save_data_to_json(filepath, search_term, location, new_items):
#     data = load_existing_data(filepath)
#     search_term = search_term.capitalize()
#     location = location.capitalize()
#
#     if search_term not in data:
#         data[search_term] = {}
#
#     if location not in data[search_term]:
#         data[search_term][location] = []
#
#     data[search_term][location].extend(new_items)
#
#     with open(filepath, 'w') as file:
#         json.dump(data, file, indent=4)
#
#
# # Function to scroll and collect items
# def scroll_and_collect_items(driver, target_items):
#     items = []
#     initial_items = 12  # Initial items loaded without scroll
#     items_per_scroll = 6  # New items per scroll
#
#     if target_items > initial_items:
#         scrolls_needed = (target_items - initial_items + items_per_scroll - 1) // items_per_scroll
#     else:
#         scrolls_needed = 0
#
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]')))
#     main_div = driver.find_element(By.CSS_SELECTOR, 'div[role="main"]')
#
#     for _ in range(scrolls_needed):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.uniform(1.0, 2.0))
#         print(f"Scrolled to bottom of page. Attempting to collect items...")
#
#     current_items = main_div.find_elements(By.TAG_NAME, 'a')
#     for a_tag in current_items[:target_items]:
#         try:
#             item_info = {
#                 'link': a_tag.get_attribute('href'),
#                 'title': a_tag.find_element(By.TAG_NAME, 'img').get_attribute('alt'),
#                 'image_url': a_tag.find_element(By.TAG_NAME, 'img').get_attribute('src')
#             }
#             items.append(item_info)
#             print(f"Collected item: {item_info['title']}")
#         except Exception as e:
#             print(f"Error extracting item: {e}")
#
#     return items
#
#
# # Main function to handle Facebook Marketplace scraping
# def launch_facebook_marketplace(location: str, search_term: str, filepath):
#     # Configure ChromeDriver path
#     chromedriver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
#     manage_driver = Service(executable_path=chromedriver_path)
#
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#
#     prefs = {"profile.managed_default_content_settings.images": 2}
#     options.add_experimental_option("prefs", prefs)
#
#     temp_dir = tempfile.mkdtemp()
#     options.add_argument(f"user-data-dir={temp_dir}")
#
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
#     options.add_argument(f"user-agent={user_agent}")
#
#     proxies = chrome_proxy(PROXY_USERNAME, PROXY_PASSWORD, ENDPOINT)
#     driver = webdriver.Chrome(service=manage_driver, options=options, seleniumwire_options=proxies)
#
#     stealth(driver,
#             languages=["en-US", "en"],
#             vendor="Google Inc.",
#             platform="Win32",
#             webgl_vendor="Intel Inc.",
#             renderer="Intel Iris OpenGL Engine",
#             fix_hairline=True,
#             )
#
#     try:
#         encoded_search_term = quote(search_term)
#         url = f'https://www.facebook.com/marketplace/{location}/search?radius=805&deliveryMethod=all&query={encoded_search_term}'
#         print(f"Navigating to {url}")
#         driver.get(url)
#         WebDriverWait(driver, 20).until(lambda x: driver.execute_script('return document.readyState') == 'complete')
#
#         items_collected = scroll_and_collect_items(driver, TARGET_ITEMS)
#
#         if items_collected:
#             print(f"Successfully collected {len(items_collected)} items in {location}.")
#             save_data_to_json(filepath, search_term, location, items_collected)
#         else:
#             print(f"No items were found in {location}.")
#
#     except Exception as e:
#         print(f"An error occurred in location {location}: {e}")
#
#     driver.quit()
#
#
# if __name__ == "__main__":
#     while True:
#         location_input = input("Please enter the location for the search (e.g., newyork): ").strip()
#         search_term_input = input("Please enter the product or item to search for (e.g., furniture): ").strip()
#         file_path = 'fb_local_items.json'
#
#         launch_facebook_marketplace(location_input, search_term_input, file_path)
#
#         continue_scraping = input("Do you want to scrape another location? (yes/no): ").strip().lower()
#         if continue_scraping != 'yes':
#             break
import time
import random
import json
import logging
from urllib.parse import quote
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import tempfile
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import sys

# Constants
PROXY_USERNAME = "yabada_djkVV"
PROXY_PASSWORD = "yuhimR42_yabada"
ENDPOINT = "pr.oxylabs.io:7777"
TARGET_ITEMS = 150
MAX_RUNS = 96

# Adjusted logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('scraping.log', encoding='utf-8')
    ]
)

# Function to set up proxies
def chrome_proxy(user: str, password: str, endpoint: str) -> dict:
    wire_options = {
        "proxy": {
            "http": f"http://{user}:{password}@{endpoint}",
            "https": f"https://{user}:{password}@{endpoint}",
        }
    }
    return wire_options

# Load existing data to append new results
def load_existing_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save the collected data to JSON
def save_data_to_json(filepath, search_term, location, new_items):
    data = load_existing_data(filepath)
    search_term = search_term.capitalize()
    location = location.capitalize()

    if search_term not in data:
        data[search_term] = {}

    if location not in data[search_term]:
        data[search_term][location] = []

    data[search_term][location].extend(new_items)

    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Function to scroll and collect items
def scroll_and_collect_items(driver, target_items):
    items = []
    initial_items = 12  # Initial items loaded without scroll
    items_per_scroll = 6  # New items per scroll

    if target_items > initial_items:
        scrolls_needed = (target_items - initial_items + items_per_scroll - 1) // items_per_scroll
    else:
        scrolls_needed = 0

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]')))
    main_div = driver.find_element(By.CSS_SELECTOR, 'div[role="main"]')

    for _ in range(scrolls_needed):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1.0, 2.0))
        logging.info(f"Scrolled to bottom of page. Attempting to collect items...")

    current_items = main_div.find_elements(By.TAG_NAME, 'a')
    for a_tag in current_items[:target_items]:
        try:
            img_tag = a_tag.find_element(By.TAG_NAME, 'img')
            item_info = {
                'link': a_tag.get_attribute('href'),
                'title': img_tag.get_attribute('alt'),
                'image_url': img_tag.get_attribute('src')
            }
            items.append(item_info)
            logging.info(f"Collected item: {item_info['title']}")
        except NoSuchElementException:
            logging.warning("Could not find <img> element inside the <a> tag. Skipping this item.")
        except Exception as e:
            logging.error(f"Error extracting item: {e}")

    return items

# Main function to handle Facebook Marketplace scraping
def launch_facebook_marketplace(location: str, search_term: str, filepath):
    # Use the ChromeDriver path provided
    chromedriver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
    manage_driver = Service(executable_path=chromedriver_path)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"user-data-dir={temp_dir}")

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    proxies = chrome_proxy(PROXY_USERNAME, PROXY_PASSWORD, ENDPOINT)
    driver = webdriver.Chrome(service=manage_driver, options=options, seleniumwire_options=proxies)

    # Apply stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    try:
        encoded_search_term = quote(search_term)
        url = f'https://www.facebook.com/marketplace/{location}/search?radius=805&deliveryMethod=all&query={encoded_search_term}'
        logging.info(f"Navigating to {url}")
        driver.get(url)
        WebDriverWait(driver, 20).until(lambda x: driver.execute_script('return document.readyState') == 'complete')

        items_collected = scroll_and_collect_items(driver, TARGET_ITEMS)

        if items_collected:
            logging.info(f"Successfully collected {len(items_collected)} items in {location}.")
            save_data_to_json(filepath, search_term, location, items_collected)
        else:
            logging.warning(f"No items were found in {location}.")

    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logging.error(f"An error occurred in location {location}: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        location_input = input("Please enter the location for the search (e.g., newyork): ").strip()
        search_term_input = input("Please enter the product or item to search for (e.g., furniture): ").strip()
        file_path = 'fb_local_items.json'

        launch_facebook_marketplace(location_input, search_term_input, file_path)

        continue_scraping = input("Do you want to scrape another location? (yes/no): ").strip().lower()
        if continue_scraping != 'yes':
            break
