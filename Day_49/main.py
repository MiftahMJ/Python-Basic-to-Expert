from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Your account details
ACCOUNT_EMAIL = "abc@gmail.com"
ACCOUNT_PASSWORD = "Your pswd"
PHONE = "your phone"

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Initialize the WebDriver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Navigate to LinkedIn Jobs page
driver.get("https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=marketing%20intern&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0")

# Allow the page to load
time.sleep(2)

# Click on the Sign-in button
sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")
sign_in_button.click()

# Wait for the login page to load and enter credentials
time.sleep(5)
email_field = driver.find_element(By.ID, "username")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

# Allow time for the login to process
time.sleep(5)

# Find all job listings on the page
all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

# Loop through each listing
for listing in all_listings:
    print("Processing a job listing...")
    listing.click()
    time.sleep(2)

    # Try to find the 'Apply' button; if not found, skip the job
    try:
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        apply_button.click()
        time.sleep(5)

        # Check if the phone number field is empty, and fill it if necessary
        phone = driver.find_element(By.CLASS_NAME, "fb-single-line-text__input")
        if phone.get_attribute("value") == "":
            phone.send_keys(PHONE)

        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")

        # Check if it's a multi-step application and skip if it is
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_elements(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button.click()

        # Close the pop-up window after submitting
        time.sleep(2)
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()

    except NoSuchElementException:
        print("No application button found, skipped.")
        continue

# Wait a moment before closing the browser
time.sleep(5)
driver.quit()
