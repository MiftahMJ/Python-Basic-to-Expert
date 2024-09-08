from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import json
import logging
from tqdm import tqdm
from urllib.parse import urljoin, urlparse

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Configure logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
    return [urljoin(current_url, link['href']) for link in soup.find_all('a', href=True)
            if is_valid_url(urljoin(current_url, link['href']), base_url)]

# Function to save the scraped content
def save_scraped_data(scraped_data, batch_num):
    filename = f"scraped_data_batch_{batch_num}.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
    logger.info(f"Batch {batch_num} saved to {filename}")

# Main scraping function using Selenium
def scrape_website(start_url, batch_size=100, total_batches=10):
    driver = get_driver()
    urls_to_process = [start_url]
    visited_urls = set([start_url])
    scraped_data = []
    batch_num = 1

    try:
        with tqdm(total=batch_size * total_batches, desc="Scraping Progress", unit="URL") as pbar:
            while batch_num <= total_batches and urls_to_process:
                batch_urls = urls_to_process[:batch_size]
                urls_to_process = urls_to_process[batch_size:]

                if not batch_urls:
                    break  # No more URLs to process

                for url in batch_urls:
                    driver.get(url)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    content = soup.get_text(separator=' ', strip=True)
                    scraped_data.append({
                        'url': url,
                        'content': content,
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    new_urls = extract_urls(soup, url, start_url)
                    urls_to_process.extend(new_urls)
                    pbar.update(1)

                save_scraped_data(scraped_data, batch_num)
                scraped_data.clear()  # Clear data for next batch
                batch_num += 1
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
    finally:
        driver.quit()

# Entry point
if __name__ == "__main__":
    start_url = "http://www.unity.de"  # The starting URL
    scrape_website(start_url)
