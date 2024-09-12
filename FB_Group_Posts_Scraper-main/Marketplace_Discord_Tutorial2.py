# Import Dependencies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pandas as pd
from bs4 import BeautifulSoup

# Configure ChromeDriver
chrome_install = ChromeDriverManager().install()
folder = os.path.dirname(chrome_install)
chromedriver_path = os.path.join(folder, "chromedriver.exe")

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--headless')  # Remove this to see the browser in action

# Initialize WebDriver
browser = webdriver.Chrome(
    service=Service(chromedriver_path),
    options=chrome_options
)

# Hardcoded login credentials (Replace with your own)
Username = "03170617459"  # Replace with your Facebook username
Password = "naha1691"  # Replace with your Facebook password


# Login function for Facebook
def facebook_login(browser, username, password):
    try:
        browser.get('https://www.facebook.com/login')
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        ).send_keys(username)
        browser.find_element(By.NAME, 'pass').send_keys(password)
        browser.find_element(By.NAME, 'login').click()
        print("Logged In!")
        return True
    except Exception as e:
        print(f"Login Failed: {e}")
        return False


# Scroll down the page to load more posts
def scroll_page(browser, scroll_limit=5):
    last_height = browser.execute_script("return document.body.scrollHeight")
    for _ in range(scroll_limit):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Extract post data with enhanced filtering
def extract_post_data(browser):
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    post_elements = soup.find_all('div', class_='x9f619')  # Adjust for correct class for posts
    posts = []

    for post in post_elements:
        try:
            # Extract author, post content, reactions, comments, images, and timestamp
            author = post.find('h2').text if post.find('h2') else 'Unknown'
            content = post.find('div', attrs={"dir": "auto"}).text if post.find('div',
                                                                                attrs={"dir": "auto"}) else 'No content'
            reactions = post.find('span', class_='x1e558r4').text if post.find('span', class_='x1e558r4') else '0'
            comments = post.find('span', class_='html-span').text if post.find('span',
                                                                               class_='html-span') else '0 comments'

            # Filter out emoji images and other irrelevant URLs
            image = post.find('img')['src'] if post.find('img') and 'emoji.php' not in post.find('img')[
                'src'] else 'No image'
            timestamp = post.find('a', {'aria-label': True}).text if post.find('a', {'aria-label': True}) else 'Unknown'

            # Add filter to exclude posts with no content and no image
            if content != 'No content' or image != 'No image':
                # Avoid duplicate entries
                if not any(p['Content'] == content and p['Author'] == author for p in posts):
                    posts.append({
                        'Author': author,
                        'Content': content,
                        'Reactions': reactions,
                        'Comments': comments,
                        'Image URL': image,
                        'Timestamp': timestamp
                    })

        except Exception as e:
            print(f"Error parsing post: {e}")

    return posts


# Save posts to a CSV file
def save_posts_to_csv(posts, filename='facebook_posts.csv'):
    df = pd.DataFrame(posts)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


# Main function
def main():
    try:
        if facebook_login(browser, Username, Password):
            # Go to the Facebook group page
            group_url = "https://www.facebook.com/groups/193804700775550"
            browser.get(group_url)
            time.sleep(5)

            # Scroll to load posts
            scroll_page(browser, scroll_limit=5)

            # Extract posts
            posts = extract_post_data(browser)

            # Save data to CSV
            save_posts_to_csv(posts)

        else:
            print("Login failed. Please check your credentials.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        browser.quit()


if __name__ == "__main__":
    main()
