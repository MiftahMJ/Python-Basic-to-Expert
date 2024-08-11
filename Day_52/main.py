import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Initialize the Service object
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Navigate to the desired URL
driver.get("https://www.instagram.com/")
print("Navigated to https://www.instagram.com/")
username = driver.find_element(By.CLASS_NAME, "_aa48")
username.send_keys("")
password = driver.find_element(By.NAME, "password")
password.send_keys("")

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()
time.sleep(50)
