from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import random
from fake_useragent import UserAgent
import schedule

# Path to your ChromeDriver
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Function to randomize comments
comments = [
    "Nice post!", "Great shot!", "Amazing picture!",
    "Wow, love this!", "Beautiful!", "This is incredible!", "Keep it up!"
]



def get_random_comment():
    return random.choice(comments)


# Function to randomize sleep intervals
def random_sleep():
    sleep_time = random.uniform(5, 15)  # Sleep between 5 and 15 seconds
    time.sleep(sleep_time)


# Set up Selenium WebDriver with user-agent rotation
def set_up_driver():
    ua = UserAgent()  # Initialize user-agent randomizer
    options = webdriver.ChromeOptions()

    # Add random user-agent to Chrome options
    options.add_argument(f"user-agent={ua.random}")

    # Set up ChromeDriver with the provided path
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver


# Function to post a comment on Instagram
def post_comment(driver, post_url):
    try:
        driver.get(post_url)
        random_sleep()  # Wait for the page to load

        # Find comment box and submit random comment
        comment_box = driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Add a comment…']")
        comment_box.send_keys(get_random_comment())

        random_sleep()  # Simulate thinking time before submitting
        submit_button = driver.find_element(By.XPATH, "//button[text()='Post']")
        submit_button.click()
        print(f"Posted comment on {post_url}")
    except Exception as e:
        print(f"Failed to post comment on {post_url}: {e}")


# Function to automate multiple comments on multiple posts
def automate_comments():
    # Replace with actual Instagram post URLs
    post_urls = [
        "https://www.instagram.com/p/POST_URL_1/",
        "https://www.instagram.com/p/POST_URL_2/",
        "https://www.instagram.com/p/POST_URL_3/"
    ]

    driver = set_up_driver()

    for post_url in post_urls:
        post_comment(driver, post_url)
        random_sleep()  # Add delay between posts

    driver.quit()


# Schedule the automation to run daily at a specific time (optional)
def schedule_automation():
    schedule.every().day.at("10:00").do(automate_comments)
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the Instagram comment automation
if __name__ == "__main__":
    automate_comments()
