from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from capsolver import Capsolver


# CapSolver API key
CAPSOLVER_API_KEY = 'CAP-BD77A472B54AE14FEFD215E8AC9CD526'

# Hardcoded credentials
username = "engrjawwad05@gmail.com"
password = "Germany09@"

# Initialize CapSolver API client
solver = Capsolver(CAPSOLVER_API_KEY)

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Start WebDriver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open the login page
driver.get("https://visa.vfsglobal.com/aze/en/ltp/login")

# Wait for the login form to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

# Fill in the email and password fields
driver.find_element(By.ID, "email").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)

# Solve the Cloudflare Captcha using CapSolver
site_key = "your-site-key-from-page"  # Replace with actual site key found in the page
captcha_solution = solver.solve_captcha({
    'type': 'turnstile',
    'websiteURL': driver.current_url,
    'websiteKey': site_key
})


# Insert the captcha response into the hidden field
driver.execute_script(f'document.getElementById("cf-chl-widget-ndzun_response").value="{captcha_solution["solution"]}"')

# Click the Sign In button
submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'mat-stroked-button')]")
submit_button.click()

# Wait for the page to load after login
sleep(5)

# You can proceed to navigate through the logged-in area of the website or scrape the desired content.

# Close the browser
driver.quit()

