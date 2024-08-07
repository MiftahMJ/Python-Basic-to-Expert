
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to be accessed
url = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
driver.get(url)

# Pause to allow for manual CAPTCHA solving
print("Please solve the CAPTCHA in the browser window.")
time.sleep(60)  # Adjust sleep time if necessary

# Extract HTML after solving CAPTCHA
html = driver.page_source
driver.quit()

# Use BeautifulSoup to parse HTML
soup = BeautifulSoup(html, "lxml")

# Print full HTML to debug
print(soup.prettify())

# Extract and print title
title_element = soup.find(id="productTitle")
if title_element:
    title = title_element.get_text(strip=True)
    print(f"Title: {title}")
else:
    print("Title element not found.")
    title = "Unknown Title"

# Extract price
# Check for different price element classes or IDs
price_element = soup.find(class_="a-price-whole")
if price_element:
    price_text = price_element.get_text(strip=True)
    print(f"Price Text: {price_text}")

    # Remove any non-numeric characters and convert to float
    try:
        price_without_currency = price_text.replace(",", "")
        price_as_float = float(price_without_currency)
        print(f"Price as Float: {price_as_float}")
    except ValueError:
        print("Error converting price to float.")
        price_as_float = None
else:
    print("Price element not found.")
    price_as_float = None

# Email details
SENDGRID_API_KEY = "Your API"
FROM_EMAIL = "your email"
TO_EMAIL = "receiver email"
BUY_PRICE = 200

# Send email if price is below BUY_PRICE
if price_as_float is not None and price_as_float < BUY_PRICE:
    message = f"{title} is now ${price_as_float:.2f}"
    url = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"

    # Create a Mail object
    mail = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject='Amazon Price Alert!',
        html_content=f'<strong>{message}</strong><br><a href="{url}">View Product</a>'
    )

    try:
        # Initialize SendGrid client and send the email
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(mail)

        # Print response details
        print(response.status_code)
        print(response.body.decode())
        print(response.headers)
    except Exception as e:
        print(f"Error sending email: {e}")
