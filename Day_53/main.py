from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Initialize the WebDriver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Zillow URL
zillow_url = "https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

# Load the Zillow page
driver.get(zillow_url)

# Allow time for the page to fully load
time.sleep(10)

# Extract listings using Selenium
all_links = driver.find_elements(By.CSS_SELECTOR, "a.list-card-link")
all_addresses = driver.find_elements(By.CSS_SELECTOR, "address.list-card-addr")
all_prices = driver.find_elements(By.CSS_SELECTOR, "div.list-card-price")

# Create lists
links = [link.get_attribute("href") for link in all_links if link.get_attribute("href") is not None]
addresses = [address.text for address in all_addresses]
prices = [price.text for price in all_prices]

# Display the scraped data
print("Links:", links)
print("Addresses:", addresses)
print("Prices:", prices)

# Google Forms URL
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeoe1zwe7ta5ZeeyW5zLSBcai1I_lCgFtAt0N0jer8aSb0VJA/viewform?usp=sf_link"

# Iterate through the scraped data and fill out the form
for i in range(len(links)):
    driver.get(google_form_url)

    # Wait for the form fields to be present
    address_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    )
    price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    # Fill the form fields with the scraped data
    address_field.send_keys(addresses[i])
    price_field.send_keys(prices[i])
    link_field.send_keys(links[i])
    submit_button.click()

    # Wait for the form to submit


# Close the browser when done
driver.quit()
time.sleep(50)