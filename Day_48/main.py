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
driver.get("https://www.python.org")
print("Navigated to https://www.python.org")

# Correct way to find elements using CSS selector
event_times = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
event_names=driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")
events={}
for n in range(len(event_times)):
    events[n]={
        "time": event_times[n].text,
        "name":event_names[n].text,
    }
print(events)



# Close the browser
driver.quit()
