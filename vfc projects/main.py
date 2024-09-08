import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import random

# Automatically install the correct version of Chromium
chromedriver_autoinstaller.install()


# Set up Selenium with undetected_chromedriver to bypass detection
def create_driver_with_chromium(proxy_address=None):
    # Set up options for Chromium
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Use headless Chromium mode if needed
    # options.add_argument("--headless")

    # If using a proxy
    if proxy_address:
        options.add_argument(f'--proxy-server={proxy_address}')

    # Use undetected Chrome driver
    driver = uc.Chrome(options=options)
    return driver


# Function to simulate human-like delays
def human_delay(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))


# Function to scroll the element into view and ensure visibility
def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)  # Give a moment for the scroll to finish


# Function to perform the login and solve the captcha using Selenium
def perform_login(driver, username, password):
    # Open the login page
    driver.get("https://visa.vfsglobal.com/npl/en/ltp/login")

    try:
        # Explicitly wait for the username field to appear and scroll it into view
        username_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))  # Modify if the selector is different
        )

        # Check if the username field is visible
        if username_field.is_displayed():
            scroll_into_view(driver, username_field)  # Scroll into view if necessary
            human_delay()
            username_field.send_keys(username)
        else:
            print("Username field is not visible or interactable.")
            return

        # Wait until the password field is clickable
        password_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))  # Modify if the selector is different
        )

        # Check if the password field is visible
        if password_field.is_displayed():
            scroll_into_view(driver, password_field)  # Scroll into view if necessary
            human_delay()
            password_field.send_keys(password)
        else:
            print("Password field is not visible or interactable.")
            return

        # Simulate human delay
        human_delay()

        # Attempt to solve the captcha by clicking the checkbox
        try:
            # Wait for the iframe that contains the captcha checkbox
            captcha_frame = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
                # Adjust the selector if needed
            )
            driver.switch_to.frame(captcha_frame)

            # Wait for the captcha checkbox to be clickable and click it
            captcha_checkbox = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))
                # Adjust the selector if needed
            )
            captcha_checkbox.click()

            print("Captcha checkbox clicked.")

            # Switch back to the main content
            driver.switch_to.default_content()

        except Exception as e:
            print(f"Error during captcha solving: {e}")

        # Simulate human delay
        human_delay()

        # Wait for the sign-in button to be clickable, scroll it into view, and click it
        submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))  # Adjust the selector if needed
        )
        scroll_into_view(driver, submit_button)  # Scroll into view if necessary
        submit_button.click()

        # Wait for the login to complete and check if the URL indicates success
        try:
            WebDriverWait(driver, 15).until(
                EC.url_contains("dashboard")  # Adjust this to the correct URL or condition
            )
            print("Login successful!")
        except Exception as e:
            print(f"Error during login: {e}")
            print("Login failed, please verify the elements and try again.")

    except Exception as e:
        print(f"Error during the form field processing: {e}")


def main():
    # Use a proxy (replace with a valid proxy or set to None if not using one)
    proxy_address = None  # "http://your-proxy-address:port"  # Replace with your proxy address if needed

    # Create the Selenium driver with Chromium
    driver = create_driver_with_chromium(proxy_address=proxy_address)

    # Provided login information
    username = "kajil41834@wikinoir.com"
    password = "Email@590jrt"

    try:
        # Perform the login using the provided info
        perform_login(driver, username, password)
    finally:
        # Close the driver once finished
        driver.quit()


if __name__ == "__main__":
    main()
