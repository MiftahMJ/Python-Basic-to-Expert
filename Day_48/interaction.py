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
driver.get("https://secure-retreat-92358.herokuapp.com/")
print("Navigated to https://secure-retreat-92358.herokuapp.com/")
articles = driver.find_element(By.CLASS_NAME, "top")
articles.send_keys("cookie")
# all_portals=driver.find_element(By.LINK_TEXT,"All portals")

search=driver.find_element(By.CLASS_NAME,"middle")
search.send_keys("Python")
email=driver.find_element(By.CLASS_NAME,"bottom")
email.send_keys("miftahjabeen@gmail.com")
enter=driver.find_element(By.CLASS_NAME,"btn")
enter.click()
# search.send_keys(Keys.Enter)
time.sleep(10)
driver.quit()