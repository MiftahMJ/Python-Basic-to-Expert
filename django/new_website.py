from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json
import logging
from tqdm import tqdm
from urllib.parse import urljoin, urlparse

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Configure logging
logging.basicConfig(filename='scraping.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems


# Initialize the Chrome WebDriver
def get_driver():
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Function to validate URLs
def is_valid_url(url, base_url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == urlparse(base_url).netloc and parsed_url.scheme in ['http', 'https']


# Extract URLs from page content
def extract_urls(soup, current_url, base_url):
    new_urls = [urljoin(current_url, link['href']) for link in soup.find_all('a', href=True)
                if is_valid_url(urljoin(current_url, link['href']), base_url)]

    logger.debug(f"Extracted {len(new_urls)} URLs from {current_url}")
    return new_urls


# Function to save the scraped content
def save_scraped_data(scraped_data, filename="scraped_data.json"):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
    logger.info(f"All data saved to {filename}")


# Main scraping function using Selenium
def scrape_website(start_url, max_urls=1000):
    driver = get_driver()
    urls_to_process = [start_url]
    visited_urls = set([start_url])
    scraped_data = []

    try:
        with tqdm(total=max_urls, desc="Scraping Progress", unit="URL") as pbar:
            while urls_to_process and len(visited_urls) <= max_urls:
                url = urls_to_process.pop(0)

                logger.debug(f"Processing URL: {url}")

                if url not in visited_urls:
                    driver.get(url)

                    # Add an explicit wait for the presence of <a> tags
                    try:
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.TAG_NAME, "a"))
                        )
                    except Exception as e:
                        logger.error(f"No <a> tags found or timeout on {url}: {e}")
                        continue

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    logger.debug(f"Page title: {soup.title.string if soup.title else 'No Title'}")

                    content = soup.get_text(separator=' ', strip=True)

                    # Append the data
                    scraped_data.append({
                        'url': url,
                        'content': content,
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    })

                    # Extract new URLs
                    new_urls = extract_urls(soup, url, start_url)
                    for new_url in new_urls:
                        if new_url not in visited_urls:
                            urls_to_process.append(new_url)

                    # Mark the URL as visited
                    visited_urls.add(url)
                    pbar.update(1)

    except Exception as e:
        logger.error(f"Error during scraping: {e}")
    finally:
        driver.quit()

    # Save all scraped data to a single JSON file
    save_scraped_data(scraped_data)


# Entry point
if __name__ == "__main__":
    start_url = "http://www.lerdon.de"  # The starting URL
    scrape_website(start_url)
