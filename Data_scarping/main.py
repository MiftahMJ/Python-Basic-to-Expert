from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

# Set up Selenium WebDriver
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the webpage
url = "https://sellviacatalog.com/product/1660119"
driver.get(url)

# Allow some time for JavaScript to load
time.sleep(5)

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Print raw HTML for debugging
print(soup.prettify())

# Extract the product title
title_tag = soup.find('h1', class_='h4', itemprop='name')  # Updated to match the new class and attribute
title = title_tag.text.strip() if title_tag else "Title Not Found"
print(f"Title: {title}")

# Extract the product description
description_tag = soup.find('div', class_='product-description')  # Adjust the class name as needed
description = description_tag.text.strip() if description_tag else "Description Not Found"
print(f"Description: {description}")

# Extract all images from `itembgr` divs
item_images = []
for item_div in soup.find_all('div', class_='itembgr'):
    img_src = item_div.get('data-img')
    if img_src:
        item_images.append(img_src)

# Extract the main image from `single_showroom` div
main_image_tag = soup.find('div', class_='single_showroom')
main_image = main_image_tag.find('img')['data-lazy'] if main_image_tag else "No Main Image Found"

# Collect all images
all_images = item_images + [main_image]
all_images_str = ", ".join(all_images) if all_images else "No Images Found"
print(f"Images: {all_images_str}")

# Extract processing time
processing_time = "Processing Time Not Found"
processing_time_div = soup.find('div', class_='single-shipping_title')
if processing_time_div:
    processing_time_span = processing_time_div.find('b', class_='name')
    if processing_time_span:
        processing_time = processing_time_div.text.replace(processing_time_span.text, '').strip()
print(f"Processing Time: {processing_time}")

# Extract the price
price_tag = soup.find('span', class_='number')  # Adjust the class name as needed
price = price_tag.text.strip() if price_tag else "Price Not Found"
print(f"Price: {price}")

# Extract all hidden fields
hidden_fields = {}
for hidden_input in soup.find_all('input', type='hidden'):
    name = hidden_input.get('name')
    value = hidden_input.get('value')
    hidden_fields[name] = value

# Prepare data for CSV
data = {
    'Title': title,
    'Description': description,
    'Images': all_images_str,
    'Processing Time': processing_time,
    'Price': price,
}

# Combine hidden fields with the data
data.update(hidden_fields)

# Write data to CSV
csv_file = 'product_details.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)

print(f"Data successfully written to {csv_file}")

