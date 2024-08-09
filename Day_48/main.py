from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Corrected path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Initialize the Service object
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Open a webpage
driver.get("https://www.amazon.com")

# Perform actions with the driver...

# Close the browser
driver.quit()
