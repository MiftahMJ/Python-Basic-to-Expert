import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Set your NopeCHA API key
API_KEY = 'I-PLHFAT53PHVC'  # Replace with your actual API key

# Updated email and password
email = 'pasha646king@gmail.com'
password = '12345'


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
    """Capture and decode the CAPTCHA image URL."""
    try:
        captcha_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//img[@id='Imageid']"))
        )
        captcha_src = captcha_element.get_attribute("src")
        print("Captcha image source URL extracted.")
        return captcha_src
    except TimeoutException:
        print("Timed out waiting for CAPTCHA image to load.")
        return None
    except NoSuchElementException as e:
        print(f"Error locating CAPTCHA element: {e}")
        return None
    except Exception as e:
        print(f"Error capturing CAPTCHA image: {e}")
        return None


def solve_captcha(captcha_url):
    """Solve CAPTCHA using the NopeCHA API."""
    if captcha_url:
        try:
            post_url = "https://api.nopecha.com/"
            post_payload = {
                'key': API_KEY,
                'type': 'textcaptcha',
                'image_data': [captcha_url],
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


def close_popup(driver):
    """Close the pop-up if it appears."""
    try:
        pop_close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@class='pop-close' and @alt='Close']"))
        )
        pop_close_button.click()
        print("Pop-up closed.")
        time.sleep(2)
    except TimeoutException:
        print("No pop-up appeared.")
    except NoSuchElementException:
        print("Pop-up close button not found.")
    except Exception as e:
        print(f"Unexpected error while closing pop-up: {e}")


def find_element_with_smart_scroll(driver, by, value):
    """Attempt to find an element by scrolling and stopping if found."""
    scroll_attempts = 0
    while scroll_attempts < 10:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except (NoSuchElementException, TimeoutException):
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)  # Adding delay for smoother scrolling
            if scroll_attempts == 5:  # Try scrolling up after 5 attempts to catch missed elements
                driver.execute_script("window.scrollBy(0, -150);")
            scroll_attempts += 1
            print(f"Scrolling... Attempt {scroll_attempts}")

    print("Element not found after smart scrolling.")
    return None


def main():
    driver = init_driver()
    driver.get("https://blsitalypakistan.com/")

    try:
        # Wait for the page to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print("Page loaded successfully.")

        # Locate and click the "Login" button to open the login form
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='https://blsitalypakistan.com/account/login' and contains(text(), 'Login')]"))
        )
        login_button.click()
        print("Login button clicked.")

        # Wait for the login page to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'submitLogin')))
        print("Login page loaded successfully.")

        # Close any pop-ups
        close_popup(driver)

        # Find email input field with smart scrolling
        email_input = find_element_with_smart_scroll(driver, By.XPATH,
                                                     "//input[@type='text' and @placeholder='Enter Email']")
        if email_input:
            email_input.send_keys(email)
        else:
            print("Email input field not found.")
            return

        # Find password input field with smart scrolling
        password_input = find_element_with_smart_scroll(driver, By.XPATH,
                                                        "//input[@type='password' and @placeholder='Enter Password']")
        if password_input:
            password_input.send_keys(password)
        else:
            print("Password input field not found.")
            return

        # Capture and solve CAPTCHA
        captcha_image_url = capture_captcha_image(driver)
        captcha_solution = solve_captcha(captcha_image_url)

        if captcha_solution:
            captcha_input = find_element_with_smart_scroll(driver, By.ID, "captcha_code_reg")
            if captcha_input:
                captcha_input.clear()
                captcha_input.send_keys(captcha_solution)

                # Submit login form
                submit_button = find_element_with_smart_scroll(driver, By.NAME, "submitLogin")
                if submit_button:
                    submit_button.click()
                    print("Login form submitted.")
                    time.sleep(5)  # Wait for response

                    # Check for login success
                    if "Dashboard" in driver.page_source:
                        print("Logged in successfully. Proceeding to book appointment.")
                        # Navigate to the appointment booking page
                        driver.get("https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment")
                        time.sleep(5)

                        # Close any pop-ups
                        close_popup(driver)

                        # Scroll down to view the appointment options
                        driver.execute_script("window.scrollBy(0, 500);")
                        time.sleep(2)

                        # Select Islamabad location
                        location_select = find_element_with_smart_scroll(driver, By.ID, "valCenterLocationId")
                        if location_select:
                            location_select.click()
                            location_select.find_element(By.XPATH,
                                                         "//option[contains(text(), 'Islamabad (Pakistan)')]").click()
                            time.sleep(5)

                        # Close any pop-ups
                        close_popup(driver)

                        # Select service type - National - Study
                        service_select = find_element_with_smart_scroll(driver, By.ID, "valCenterLocationTypeId")
                        if service_select:
                            service_select.click()
                            service_select.find_element(By.XPATH,
                                                        "//option[contains(text(), 'National - Study')]").click()
                            time.sleep(5)

                        # Finalize the appointment by solving the final CAPTCHA
                        captcha_image_url = capture_captcha_image(driver)
                        captcha_solution = solve_captcha(captcha_image_url)
                        if captcha_solution:
                            final_captcha_input = find_element_with_smart_scroll(driver, By.ID, "captcha_code_reg")
                            if final_captcha_input:
                                final_captcha_input.clear()
                                final_captcha_input.send_keys(captcha_solution)
                                print("Final CAPTCHA entered.")

                                # Uncomment the next line to submit the form automatically
                                # submit_button = find_element_with_smart_scroll(driver, By.NAME, "submit")
                                # submit_button.click()

                    else:
                        print("Login failed. Please check credentials and try again.")
                else:
                    print("Submit button not found.")
            else:
                print("CAPTCHA input field not found.")
        else:
            print("Failed to solve CAPTCHA.")
    except TimeoutException as e:
        print(f"Error: Page did not load within the expected time: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
