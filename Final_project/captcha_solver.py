import random
import time
from datetime import datetime

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set your NopeCHA API key
API_KEY = 'I-PLHFAT53PHVC'  # Replace with your actual API key

MAX_CAPTCHA_ATTEMPTS = 3

def init_driver():
    """Initialize the Chrome WebDriver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def capture_captcha_image(driver):
    """Capture and decode the CAPTCHA image from the style attribute."""
    try:
        captcha_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//captcha/div[contains(@style, 'background')]"))
        )
        style_attribute = captcha_element.get_attribute("style")
        base64_prefix = "data:image/jpg;base64,"
        start_index = style_attribute.find(base64_prefix)
        if start_index != -1:
            captcha_base64 = style_attribute[start_index + len(base64_prefix):].split("')")[0]
            print("Base64 CAPTCHA image extracted.")
            return captcha_base64
        else:
            print("CAPTCHA image is not base64 encoded.")
            return None
    except TimeoutException:
        print("Timed out waiting for CAPTCHA image to load.")
        return None
    except NoSuchElementException as e:
        print(f"Error locating CAPTCHA element: {e}")
        return None
    except Exception as e:
        print(f"Error capturing CAPTCHA image: {e}")
        return None

def solve_captcha(captcha_base64):
    """Solve CAPTCHA using the NopeCHA API."""
    if captcha_base64:
        try:
            post_url = "https://api.nopecha.com/"
            post_payload = {
                'key': API_KEY,
                'type': 'textcaptcha',
                'image_data': [captcha_base64],
            }

            print("Sending CAPTCHA to NopeCHA for solving...")
            post_response = requests.post(post_url, json=post_payload)
            post_result = post_response.json()
            print(f"POST Response: {post_result}")

            if 'data' in post_result:
                solution_id = post_result['data']
                get_payload = {
                    'key': API_KEY,
                    'id': solution_id,
                }

                # Wait for CAPTCHA solution to be ready
                time.sleep(7)  # Increased wait time

                print("Retrieving CAPTCHA solution from NopeCHA...")
                for attempt in range(5):  # Try multiple times to get the solution
                    get_response = requests.get(post_url, params=get_payload)
                    if get_response.status_code == 200:
                        try:
                            get_result = get_response.json()
                            print(f"GET Response: {get_result}")

                            if 'data' in get_result:
                                solution = get_result['data'][0]
                                print(f"Captcha solved: {solution}")
                                return solution
                            elif get_result.get('error') == 14:
                                print("Incomplete job, waiting before retrying...")
                                time.sleep(3)  # Wait before retrying
                            elif get_result.get('error') == 10:
                                print("Invalid request error received, possible incorrect parameters.")
                                break  # Break loop if there is an invalid request error
                            else:
                                print(f"Failed to retrieve CAPTCHA solution: {get_result}")
                                return None
                        except ValueError:
                            print(f"Failed to parse JSON response: {get_response.text}")
                            return None
                    else:
                        print(f"Failed to get response from API, status code: {get_response.status_code}")
                        print(f"Response text: {get_response.text}")
                        time.sleep(5)  # Wait before retrying

                return None
            else:
                print(f"Failed to submit CAPTCHA challenge: {post_result}")
                return None

        except Exception as e:
            print(f"Error solving CAPTCHA: {e}")
            return None
    else:
        print("No CAPTCHA image captured.")
        return None

def solve_captcha_with_retry(driver):
    """Solve the CAPTCHA with retry mechanism."""
    attempts = 0
    while attempts < MAX_CAPTCHA_ATTEMPTS:
        captcha_base64 = capture_captcha_image(driver)
        if not captcha_base64:
            return False

        captcha_solution = solve_captcha(captcha_base64)
        if not captcha_solution:
            attempts += 1
            continue

        captcha_input = driver.find_element(By.ID, "appointment_captcha_day_captchaText")
        captcha_input.clear()
        captcha_input.send_keys(captcha_solution)
        print("CAPTCHA entered.")

        submit_button = driver.find_element(By.ID, "appointment_captcha_day_appointment_showDay")
        submit_button.click()
        time.sleep(5)  # Wait for the next page to load

        # Check if CAPTCHA failed
        if "The entered text was wrong" in driver.page_source:
            print("CAPTCHA failed. Retrying...")
            attempts += 1
            continue

        print("CAPTCHA solved successfully.")
        return True

    print("Failed to solve CAPTCHA after several attempts.")
    return False

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

