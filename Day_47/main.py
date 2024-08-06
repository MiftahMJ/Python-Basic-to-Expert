# import requests
# from bs4 import BeautifulSoup
# import lxml
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
#
# # URL and headers
# URL = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
# }
#
# # Send GET request
# response = requests.get(URL, headers=headers)
# soup = BeautifulSoup(response.content, "lxml")
#
# # Extract and print title
# title = soup.find(id="productTitle").get_text().strip()
# print(f"Title: {title}")
#
# # Extract price
# price_element = soup.find(class_="a-offscreen")
# if price_element:
#     price_text = price_element.get_text(strip=True)
#     print(f"Price Text: {price_text}")
#
#     # Remove the dollar sign and convert to float
#     try:
#         price_without_currency = price_text.replace("$", "").replace(",", "")
#         price_as_float = float(price_without_currency)
#         print(f"Price as Float: {price_as_float}")
#     except ValueError:
#         print("Error converting price to float.")
#         price_as_float = None
# else:
#     print("Price element not found.")
#     price_as_float = None
#
# # Email details
# SENDGRID_API_KEY = "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"
# FROM_EMAIL = "miftahjabeen@gmail.com"
# TO_EMAIL = "avengerpak77@gmail.com"
# BUY_PRICE = 200
#
# # Send email if price is below BUY_PRICE
# if price_as_float is not None and price_as_float < BUY_PRICE:
#     message = f"{title} is now ${price_as_float:.2f}"
#     url = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
#
#     # Create a Mail object
#     mail = Mail(
#         from_email=FROM_EMAIL,
#         to_emails=TO_EMAIL,
#         subject='Amazon Price Alert!',
#         html_content=f'<strong>{message}</strong><br><a href="{url}">View Product</a>'
#     )
#
#     try:
#         # Initialize SendGrid client and send the email
#         sg = SendGridAPIClient(SENDGRID_API_KEY)
#         response = sg.send(mail)
#
#         # Print response details
#         print(response.status_code)
#         print(response.body.decode())
#         print(response.headers)
#     except Exception as e:
#         print(f"Error sending email: {e}")
import requests
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# URL and headers
URL = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

# Send GET request
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

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
price_element = soup.find(class_="a-offscreen")
if price_element:
    price_text = price_element.get_text(strip=True)
    print(f"Price Text: {price_text}")

    # Remove the dollar sign and convert to float
    try:
        price_without_currency = price_text.replace("$", "").replace(",", "")
        price_as_float = float(price_without_currency)
        print(f"Price as Float: {price_as_float}")
    except ValueError:
        print("Error converting price to float.")
        price_as_float = None
else:
    print("Price element not found.")
    price_as_float = None

# Email details
SENDGRID_API_KEY = "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"
FROM_EMAIL = "miftahjabeen@gmail.com"
TO_EMAIL = "avengerpak77@gmail.com"
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
