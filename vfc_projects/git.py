# Import Dependencies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import lxml.html
import os

# Your Facebook username and password
Username = '03170617459'  # Replace with your own username
Password = 'naha1691'  # Replace with your own password

# Configure ChromeDriver
chrome_install = ChromeDriverManager().install()
folder = os.path.dirname(chrome_install)
chromedriver_path = os.path.join(folder, "chromedriver.exe")

chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--headless')  # If you want to see the browser, comment this line out

# Initialize Chrome WebDriver
browser = webdriver.Chrome(
    service=Service(chromedriver_path),
    options=chrome_options
)


# Facebook login function
def facebook_login(browser, username, password):
    browser.get('https://www.facebook.com/login')

    try:
        # Locate email input field and enter the username
        email_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(username)

        # Locate password input field and enter the password
        password_input = browser.find_element(By.NAME, 'pass')
        password_input.send_keys(password)

        # Locate the login button and click it
        login_button = browser.find_element(By.NAME, 'login')
        login_button.click()

        print("Logged In!")
        return True

    except Exception as e:
        print(f"Login Failed: {e}")
        return False


# Function to scroll down the page and load more posts
def scroll_page(browser, scroll_limit=5):
    last_height = browser.execute_script("return document.body.scrollHeight")
    action = ActionChains(browser)

    for _ in range(scroll_limit):
        # Scroll to the bottom
        action.send_keys(webdriver.common.keys.Keys.END).perform()
        time.sleep(5)  # Wait for new posts to load

        # Check for page height changes
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached end of page.")
            break
        last_height = new_height


# Function to extract post data
def extract_post_data(browser):
    html = browser.page_source
    root = lxml.html.fromstring(html)

    post_elements = root.cssselect(
        'div.x9f619.x1n2onr6.x1ja2u2z.x1jx94hy.x1qpq9i9.xdney7k.xu5ydu1.xt3gfkd.xh8yej3.x6ikm8r.x10wlt62.xquyuld'
    )

    post_list = []
    print(f"Number of posts found: {len(post_elements)}")

    for post_element in post_elements:
        try:
            post_html = lxml.html.tostring(post_element).decode('utf-8')
            post_list.append(post_html)
        except Exception as e:
            print(f"Error parsing post: {e}")

    return post_list


# Function to save posts to a file
def save_posts_to_file(posts, filename='scraped_posts.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")


# Main function to log in, scroll, and scrape posts
def main():
    try:
        if facebook_login(browser, Username, Password):
            # After login, go to the Facebook group
            group_url = "https://www.facebook.com/groups/ConsumerWatchdogBW"
            browser.get(group_url)
            time.sleep(5)

            # Scroll down the page to load more posts
            scroll_page(browser, scroll_limit=5)

            # Extract post data
            posts = extract_post_data(browser)

            # Save the posts to a JSON file
            save_posts_to_file(posts)

        else:
            print("Login failed. Please check your credentials.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        browser.quit()


if __name__ == "__main__":
    main()
