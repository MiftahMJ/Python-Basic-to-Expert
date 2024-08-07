**Amazon Price Tracker and Alert**

**Overview**

The Amazon Price Tracker and Alert is a Python application designed to monitor the price of a specific product on Amazon and send an email alert when the price drops below a specified threshold. This tool combines web scraping with email notifications to help users track and manage their purchases more effectively.

**Features**

**Web Scraping:** Utilizes Selenium WebDriver and BeautifulSoup to scrape product details from Amazon.
**Price Monitoring**: Extracts and processes the product price to monitor price changes.
**Email Notifications**: Sends an email alert using SendGrid when the product price drops below the user-defined threshold.
**CAPTCHA Handling**: Pauses for manual CAPTCHA solving to ensure uninterrupted access to the product page.
**Requirements**

Python 3.x
selenium
beautifulsoup4
lxml
sendgrid
webdriver_manager
A SendGrid account for email notifications
**Setup**

**Install Dependencies:**

Make sure you have the required packages installed. You can install them using pip:

**bash**
Copy code
pip install selenium beautifulsoup4 lxml sendgrid webdriver_manager

**Get SendGrid API Key:**

Sign up for a SendGrid account and obtain your API key. Replace YOUR_SENDGRID_API_KEY in the code with your actual API key.

**Update Email Settings:**

Replace FROM_EMAIL and TO_EMAIL in the code with your email addresses. Ensure that FROM_EMAIL is a verified email address on your SendGrid account.

**Run the Application:**

Execute the script to start monitoring the product price:

**bash**
Copy code
python main.py
Follow the instructions to solve the CAPTCHA in the browser window.

**Usage**

The application will open a browser window and navigate to the specified Amazon product page.
Solve any CAPTCHA that appears in the browser window to proceed.
The script will then scrape the product information and check if the price is below the defined threshold.
If the price is below the threshold, an email notification will be sent.

**Notes**
Make sure to handle the CAPTCHA manually within the allotted time.
Adjust the sleep time if necessary based on how quickly you can solve the CAPTCHA.
**License**

This project is licensed under the MIT License - see the LICENSE file for details.
![Untitled video - Made with Clipchamp (6)](https://github.com/user-attachments/assets/5bc1ebfe-661a-4eaa-a441-346add82d134)
