# utils.py

import random
import time
from datetime import datetime
from selenium.webdriver.common.by import By

def scroll_to_element(driver, element):
    """Scroll the page until the element is in view."""
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
    time.sleep(2)  # Wait for scroll animation to complete

def select_random_date(driver):
    """Select a random date for the calendar input."""
    # Generate a random date in the past 100 years (assuming date format dd.mm.yyyy)
    start_date = datetime(1924, 1, 1)
    end_date = datetime(2004, 12, 31)
    random_date = start_date + (end_date - start_date) * random.random()
    random_date_str = random_date.strftime("%d.%m.%Y")

    # Use JavaScript to set the date directly
    date_input = driver.find_element(By.ID, "fields1content")
    driver.execute_script(f"arguments[0].value = '{random_date_str}';", date_input)
    print(f"Random date selected: {random_date_str}")
    time.sleep(1)  # Pause to simulate realistic interaction

def read_urls(file_path):
    """Read URLs from a text file and return as a list."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]
