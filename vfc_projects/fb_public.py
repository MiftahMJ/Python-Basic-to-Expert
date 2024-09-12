#
# from selenium import webdriver
# from selenium.common import TimeoutException, NoSuchElementException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# import time
#
# username = "03170617459"
# password = "naha1691"
#
# # Path to the ChromeDriver executable
# chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
#
# # Set up ChromeDriver
# service = Service(executable_path=chrome_driver_path)
# driver = webdriver.Chrome(service=service)
#
#
# def login_facebook(driver):
#     driver.get("https://www.facebook.com/")
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(username)
#     driver.find_element(By.ID, "pass").send_keys(password)
#     driver.find_element(By.NAME, "login").click()
#     time.sleep(5)  # Adjust sleep time based on loading speed
#
#
# def navigate_to_group(driver, group_url):
#     driver.get(group_url)
#     WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#     print(f"Successfully navigated to the group: {group_url}")
#
#
# def scroll_down(driver, num_scrolls=5, delay=2):
#     """ Scroll down to load more content. """
#     for _ in range(num_scrolls):
#         driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
#         time.sleep(delay)  # Adjust delay if needed for slower/faster loading
#
#
# def fetch_group_posts(driver):
#     post_data_list = []
#     try:
#         # Wait for the group feed to be loaded
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
#         print("Group feed located, starting to extract posts.")
#
#         # Scroll down to load more posts
#         scroll_down(driver, num_scrolls=5)
#
#         # Find posts in the feed after scrolling
#         posts = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div')
#         if not posts:
#             print("No posts found in the group feed.")
#             return post_data_list
#
#         print(f"Found {len(posts)} posts.")
#         for index, post in enumerate(posts[:5]):  # Limit to first 5 posts
#             post_data = extract_post_data(post)
#             if post_data:
#                 print(f"Post {index + 1}: {post_data}")
#                 post_data_list.append(post_data)
#
#     except TimeoutException:
#         print("Error: Group feed not found or took too long to load.")
#
#     return post_data_list
#
#
# def extract_post_data(post_element):
#     try:
#         # Adding wait to ensure content is loaded
#         WebDriverWait(post_element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span strong span')))
#
#         # Extract author
#         try:
#             author = post_element.find_element(By.CSS_SELECTOR, 'span strong span').text
#         except NoSuchElementException:
#             author = "Unknown"
#
#         # Extract post content (adjust selector as necessary based on updated structure)
#         try:
#             post_content = post_element.find_element(By.CSS_SELECTOR, 'div[role="article"] div[dir="auto"]').text
#         except NoSuchElementException:
#             post_content = "No content found"
#
#         # Extract timestamp
#         try:
#             post_time = post_element.find_element(By.CSS_SELECTOR, 'span[data-testid="timestamp"]').text
#         except NoSuchElementException:
#             post_time = "No timestamp"
#
#         # Extract images (optional)
#         try:
#             images = post_element.find_elements(By.CSS_SELECTOR, 'img')
#             image_urls = [img.get_attribute('src') for img in images]
#         except NoSuchElementException:
#             image_urls = []
#
#         return {
#             'author': author,
#             'content': post_content,
#             'time': post_time,
#             'images': image_urls,
#         }
#
#     except Exception as e:
#         print(f"Error while extracting post data: {e}")
#         return None
#
#
# def main():
#     try:
#         login_facebook(driver)
#         group_url = "https://www.facebook.com/groups/193804700775550/"
#         navigate_to_group(driver, group_url)
#         posts_data = fetch_group_posts(driver)
#         for post in posts_data:
#             print(post)
#
#     finally:
#         driver.quit()
#
#
# if __name__ == "__main__":
#     main()
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json

# Facebook credentials
username = "03170617459"
password = "naha1691"

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Chaudhry Traders\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Set up ChromeDriver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Login to Facebook
def login_facebook(driver):
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(username)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()
    time.sleep(5)  # Adjust sleep time based on loading speed

# Navigate to the Facebook group
def navigate_to_group(driver, group_url):
    driver.get(group_url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print(f"Successfully navigated to the group: {group_url}")

# Scroll down to load more posts
def scroll_down(driver, num_scrolls=5, delay=2):
    """ Scroll down to load more content. """
    for _ in range(num_scrolls):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(delay)  # Adjust delay if needed for slower/faster loading

# Fetch group posts
def fetch_group_posts(driver):
    post_data_list = []
    try:
        # Wait for the group feed to be loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
        print("Group feed located, starting to extract posts.")

        # Scroll down to load more posts
        scroll_down(driver, num_scrolls=5)

        # Find posts in the feed after scrolling
        posts = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
        if not posts:
            print("No posts found in the group feed.")
            return post_data_list

        print(f"Found {len(posts)} posts.")
        for index, post in enumerate(posts[:5]):  # Limit to first 5 posts
            post_data = extract_post_data(post)
            if post_data:
                print(f"Post {index + 1}: {post_data}")
                post_data_list.append(post_data)

    except TimeoutException:
        print("Error: Group feed not found or took too long to load.")

    return post_data_list

# Extract data from a post
def extract_post_data(post_element):
    try:
        # Extract author
        try:
            author = post_element.find_element(By.CSS_SELECTOR, 'h3 a').text
        except NoSuchElementException:
            author = "Unknown"

        # Extract post content
        try:
            post_content = post_element.find_element(By.CSS_SELECTOR, 'div[data-ad-preview="message"]').text
        except NoSuchElementException:
            post_content = "No content found"

        # Extract timestamp
        try:
            post_time = post_element.find_element(By.TAG_NAME, 'abbr').get_attribute('title')
        except NoSuchElementException:
            post_time = "No timestamp"

        # Extract images (optional)
        try:
            images = post_element.find_elements(By.CSS_SELECTOR, 'img')
            image_urls = [img.get_attribute('src') for img in images]
        except NoSuchElementException:
            image_urls = []

        # Extract likes
        try:
            likes = post_element.find_element(By.CSS_SELECTOR, 'span[aria-label*="Like"]').get_attribute('aria-label')
        except NoSuchElementException:
            likes = "0"

        # Extract shares
        try:
            shares = post_element.find_element(By.CSS_SELECTOR, 'span[aria-label*="share"]').get_attribute('aria-label')
        except NoSuchElementException:
            shares = "0"

        # Extract comments
        try:
            comments = post_element.find_element(By.CSS_SELECTOR, 'a[aria-label*="comment"]').text
        except NoSuchElementException:
            comments = "0 Comments"

        return {
            'author': author,
            'content': post_content,
            'time': post_time,
            'images': image_urls,
            'likes': likes,
            'shares': shares,
            'comments': comments
        }

    except StaleElementReferenceException as e:
        print(f"Error while extracting post data: {e}")
        return None

# Save scraped posts to JSON
def save_posts_to_json(post_data_list, filename="scraped_posts.json"):
    """ Save the scraped posts to a JSON file. """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(post_data_list, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

# Main function to run the script
def main():
    try:
        login_facebook(driver)
        group_url = "https://www.facebook.com/groups/193804700775550/"
        navigate_to_group(driver, group_url)
        posts_data = fetch_group_posts(driver)
        save_posts_to_json(posts_data)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
