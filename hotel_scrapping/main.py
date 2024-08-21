from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Initialize the Service object
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

def click_show_more():
    """Click the 'Show More' button until it's no longer available."""
    while True:
        try:
            # Wait for the "Show More" button to be clickable
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show more hotels')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)  # Scroll to button
            show_more_button.click()
            time.sleep(3)  # Wait for new content to load
        except Exception as e:
            print(f"No more 'Show More' button found or error: {e}")
            break

def scrape_resortpass(url):
    """Scrape hotel information from the given URL."""
    driver.get(url)
    time.sleep(5)  # Initial wait for page load

    click_show_more()  # Click 'Show More' to load all hotels

    # Get page source and parse with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Adjust selectors as needed
    hotel_names = [element.get_text(strip=True) for element in soup.find_all('h2', class_='mb-0 w-full text-19 leading-7 font-rp-pn-semi-bold px-6 d:px-0 d:text-22 d:w-3/4 d:-mt-1 d:mb-10px')]
    states = [element.get_text(strip=True) for element in soup.find_all('div', class_='hidden mb-2 d:block text-11 font-rp-pn-semi-bold uppercase text-custom-gray-2 tracking-0.6')]
    tags = [element.get_text(strip=True) for element in soup.find_all('span', class_='h-7 text-15 bg-rp-primary-new flex flex-shrink-0 font-medium items-center justify-center px-1.5 py-2 mr-2 rounded-md text-white -tracking-0.02em')]

    if not hotel_names:
        print("No hotel names found. Check the class name or tag used.")

    length = min(len(hotel_names), len(states), len(tags))

    for i in range(length):
        print(f"Hotel Name: {hotel_names[i]}")
        print(f"Tags: {tags[i]}")
        print(f"State: {states[i]}")
        print()

if __name__ == "__main__":
    url = "https://www.resortpass.com/hotel-day-passes/Miami-14"
    scrape_resortpass(url)
    driver.quit()
