from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep

# Adjusted ChromeDriver path
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Setup ChromeDriver
service = Service(executable_path=chrome_driver_path)
options = Options()
# Preventing detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=service, options=options)

# Modify the WebDriver's navigator property to hide automation flag
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

try:
    # Open Wikipedia homepage
    driver.get("https://www.wikipedia.org/")
    sleep(2)  # Wait for the page to load

    # Find the Commons link by its class and text, then click it
    commons_link = driver.find_element(By.XPATH, "//a[contains(@class, 'other-project-link') and contains(., 'Commons')]")
    commons_link.click()
    sleep(2)  # Wait for the page to load after clicking

    # Print current URL after clicking to verify
    print(f"Current URL: {driver.current_url}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
