#
# import time
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
#
# # Set your NopeCHA API key
# API_KEY = 'I-PLHFAT53PHVC'  # Replace with your actual API key
#
# # Initialize WebDriver
# def init_driver():
#     """Initialize the Chrome WebDriver with options."""
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#
#     chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
#     service = Service(executable_path=chrome_driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     return driver
#
# def capture_captcha_image(driver):
#     """Capture and decode the CAPTCHA image from the style attribute."""
#     try:
#         # Wait until the CAPTCHA image's parent <div> is present and then find it
#         captcha_element = WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha > div[id^="_"]'))
#         )
#
#         # Check if the CAPTCHA is visible
#         if captcha_element.is_displayed():
#             # Extract the 'style' attribute which contains the base64 encoded image
#             style_attribute = captcha_element.get_attribute("style")
#
#             # Look for the base64 encoded image in the style attribute
#             base64_prefix = "data:image/jpg;base64,"
#             start_index = style_attribute.find(base64_prefix)
#             if start_index != -1:
#                 # Extract the base64 string from the 'style' attribute
#                 captcha_base64 = style_attribute[start_index + len(base64_prefix):].split("')")[0]
#                 print("Base64 CAPTCHA image extracted.")
#                 return captcha_base64
#             else:
#                 print("CAPTCHA image is not base64 encoded.")
#                 return None
#         else:
#             print("CAPTCHA image is not visible.")
#             return None
#
#     except TimeoutException:
#         print("Timed out waiting for CAPTCHA image to load. Check if the CSS selector is correct or if the CAPTCHA image loads after interaction.")
#         print("Current page source:")
#         print(driver.page_source)  # Print the page source for debugging
#         return None
#     except NoSuchElementException as e:
#         print(f"Error locating CAPTCHA element: {e}")
#         return None
#     except Exception as e:
#         print(f"Error capturing CAPTCHA image: {e}")
#         return None
#
# def solve_captcha(captcha_base64):
#     """Solve CAPTCHA using the NopeCHA API."""
#     if captcha_base64:
#         try:
#             # Step 1: Submit the CAPTCHA challenge
#             post_url = "https://api.nopecha.com/"
#             post_payload = {
#                 'key': API_KEY,
#                 'type': 'textcaptcha',
#                 'image_data': [captcha_base64],
#             }
#
#             post_response = requests.post(post_url, json=post_payload)
#             post_result = post_response.json()
#             print(f"POST Response: {post_result}")
#
#             if 'data' in post_result:
#                 # Step 2: Retrieve the solution using the 'data' value from POST response
#                 solution_id = post_result['data']
#                 get_payload = {
#                     'key': API_KEY,
#                     'id': solution_id,
#                 }
#
#                 get_response = requests.get(post_url, params=get_payload)
#                 get_result = get_response.json()
#                 print(f"GET Response: {get_result}")
#
#                 if 'data' in get_result:
#                     print(f"Captcha solved: {get_result['data'][0]}")
#                     return get_result['data'][0]
#                 else:
#                     print(f"Failed to retrieve CAPTCHA solution: {get_result}")
#                     return None
#             else:
#                 print(f"Failed to submit CAPTCHA challenge: {post_result}")
#                 return None
#
#         except Exception as e:
#             print(f"Error solving CAPTCHA: {e}")
#             return None
#     else:
#         print("No CAPTCHA image captured.")
#         return None
#
# def main():
#     url = "https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=kara&realmId=967&categoryId=2801&dateStr=23.09.2024&openingPeriodId=68490"
#
#     driver = init_driver()
#     driver.get(url)
#
#     # Allow time for the page to load fully
#     time.sleep(10)  # Increased wait time to ensure the page and CAPTCHA load
#
#     captcha_base64 = capture_captcha_image(driver)
#     captcha_solution = solve_captcha(captcha_base64)
#
#     if captcha_solution:
#         try:
#             captcha_input = driver.find_element(By.ID, "appointment_captcha_day_captchaText")  # Adjusted ID for the input field
#             captcha_input.send_keys(captcha_solution)
#
#             submit_button = driver.find_element(By.ID, "appointment_captcha_day_appointment_showDay")  # Adjusted selector for submit button
#             submit_button.click()
#
#             print("Form submitted.")
#         except NoSuchElementException as e:
#             print(f"Error finding input field or submit button: {e}")
#         except Exception as e:
#             print(f"Error during form submission: {e}")
#
#     # Close the driver
#     driver.quit()
#
# if __name__ == "__main__":
#     main()


import time
import requests
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from io import BytesIO
from PIL import Image

# Set your NopeCHA API key
API_KEY = 'I-PLHFAT53PHVC'  # Replace with your actual API key

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
            EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha > div[id^="_"]'))
        )
        if captcha_element.is_displayed():
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
        else:
            print("CAPTCHA image is not visible.")
            return None
    except TimeoutException:
        print("Timed out waiting for CAPTCHA image to load. Check if the CSS selector is correct or if the CAPTCHA image loads after interaction.")
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
                time.sleep(5)  # Wait for a few seconds before checking for the solution

                print("Retrieving CAPTCHA solution from NopeCHA...")
                for attempt in range(5):  # Try multiple times to get the solution
                    get_response = requests.get(post_url, params=get_payload)
                    get_result = get_response.json()
                    print(f"GET Response: {get_result}")

                    if 'data' in get_result:
                        solution = get_result['data'][0]
                        print(f"Captcha solved: {solution}")
                        return solution
                    elif get_result.get('error') == 14:
                        print("Incomplete job, waiting before retrying...")
                        time.sleep(3)  # Wait before retrying
                    else:
                        print(f"Failed to retrieve CAPTCHA solution: {get_result}")
                        return None
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

def solve_captcha_with_retry(driver, max_retries=3):
    """Try to solve the CAPTCHA with retries if the solution is incorrect."""
    for attempt in range(max_retries):
        print(f"Solving CAPTCHA: Attempt {attempt + 1}")
        captcha_base64 = capture_captcha_image(driver)
        if captcha_base64:
            captcha_solution = solve_captcha(captcha_base64)
            if captcha_solution:
                print(f"CAPTCHA Solution Attempt {attempt + 1}: {captcha_solution}")
                return captcha_solution
        print(f"Retrying CAPTCHA solving ({attempt + 1}/{max_retries})...")
        driver.refresh()  # Refresh the page to get a new CAPTCHA
    print("Failed to solve CAPTCHA after maximum retries.")
    return None

def check_submission_success(driver):
    """Check if the form submission was successful or if CAPTCHA needs to be retried."""
    try:
        # Wait for a specific success message or element to confirm successful submission
        wait = WebDriverWait(driver, 15)
        success_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successful')]")))
        if success_element:
            print("CAPTCHA solved correctly, and form submitted successfully.")
        else:
            print("CAPTCHA solution might be incorrect, or form submission failed.")
    except TimeoutException:
        print("No success message found. It seems the CAPTCHA solution was incorrect. Retrying...")
        driver.refresh()

def validate_submission(driver):
    """Check if the form submission was successful based on specific conditions."""
    try:
        success_indicator = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Appointment available')]"))
        )
        print("Appointment available message found, form submission successful.")
        return True
    except TimeoutException:
        print("Appointment available message not found, form submission failed.")
        return False

def main():
    url = "https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=kara&realmId=967&categoryId=2801&dateStr=23.09.2024&openingPeriodId=68490"
    driver = init_driver()
    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print("Page loaded successfully.")

        captcha_solution = solve_captcha_with_retry(driver)
        if captcha_solution:
            try:
                captcha_input = driver.find_element(By.ID, "appointment_captcha_day_captchaText")
                captcha_input.clear()
                captcha_input.send_keys(captcha_solution)

                submit_button = driver.find_element(By.ID, "appointment_captcha_day_appointment_showDay")
                submit_button.click()

                print("Form submitted.")

                if not validate_submission(driver):
                    print("Retrying due to failed form submission.")
                    driver.refresh()

            except NoSuchElementException as e:
                print(f"Error finding input field or submit button: {e}")
            except Exception as e:
                print(f"Error during form submission: {e}")

    except TimeoutException as e:
        print(f"Error: Page did not load within the expected time: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
