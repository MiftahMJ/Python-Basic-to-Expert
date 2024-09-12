import time
import requests
from playwright.sync_api import sync_playwright

# Hardcoded credentials
username = "engrjawwad05@gmail.com"
password = "Germany09@"

# CapSolver API key
CAPSOLVER_API_KEY = 'CAP-BD77A472B54AE14FEFD215E8AC9CD526'

# Function to request CAPTCHA solving via CapSolver API
def solve_captcha(site_key, page_url):
    # Send a CAPTCHA request to CapSolver
    captcha_request_url = "https://api.capsolver.com/solve"

    data = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "NoCaptchaTaskProxyless",
            "websiteURL": page_url,
            "websiteKey": site_key
        }
    }

    # Request the task
    response = requests.post(captcha_request_url, json=data)
    result = response.json()

    if result.get("taskId"):
        task_id = result["taskId"]
        print(f"Task created: {task_id}. Waiting for CAPTCHA to be solved...")

        # Poll for the result
        get_result_url = "https://api.capsolver.com/getTaskResult"
        while True:
            result_response = requests.post(get_result_url, json={"clientKey": CAPSOLVER_API_KEY, "taskId": task_id})
            result_data = result_response.json()

            if result_data.get("status") == "ready":
                print("CAPTCHA solved!")
                return result_data["solution"]["gRecaptchaResponse"]

            print("CAPTCHA not yet solved, waiting...")
            time.sleep(5)  # Wait 5 seconds before checking again
    else:
        print(f"Failed to create CAPTCHA task: {result.get('errorDescription')}")
        return None

# Function to reject cookies if the "Reject All" button appears
def reject_cookies(page):
    try:
        # Check if the "Reject All" button is present
        page.wait_for_selector('#onetrust-reject-all-handler', timeout=5000)
        page.click('#onetrust-reject-all-handler')
        print("Rejected cookies.")
    except:
        print("No 'Reject All' button found, proceeding...")

# Main function to handle login and appointment checking
def run(playwright):
    # Launch browser (Chromium or Firefox)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Open the login page
    page.goto("https://visa.vfsglobal.com/aze/en/ltp/application-detail")

    # Reject cookies if prompted
    reject_cookies(page)

    # If there's an iframe for the login form, switch to it
    try:
        page.wait_for_selector('iframe', timeout=10000)
        iframe = page.frame_locator("iframe")
        iframe.wait_for_selector('input[name="username"]')  # Ensure the frame is loaded
        print("Switched to iframe.")
    except Exception as e:
        print(f"No iframe found, proceeding without switching. Error: {e}")

    # Fill in the login details
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)

    # Solve the CAPTCHA
    site_key = "your_site_key_here"  # You will need to inspect and get the actual site key from the HTML
    token = solve_captcha(site_key, page.url)
    if token:
        # Inject the CAPTCHA token into the page
        page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML="{token}";')

        # Submit the login form
        page.click('#login-button')

        # Wait for navigation to the next page
        page.wait_for_timeout(5000)

        # Check for appointments continuously
        while True:
            try:
                # Check if appointments are available
                appointment_status = page.inner_text("#appointment-status")
                if "No appointments available" in appointment_status:
                    print("No appointments available, refreshing...")
                    page.reload()
                    time.sleep(60)  # Wait a minute before checking again
                else:
                    print("Appointment found!")
                    fill_form(page)
                    break
            except Exception as e:
                print(f"Error while checking appointments: {e}")
                page.reload()
                time.sleep(60)

    # Close the browser
    browser.close()

# Function to fill the form if an appointment is found
def fill_form(page):
    print("Filling the form with provided details...")
    page.fill('input[name="field_name"]', "value")
    page.click('#submit-button')

# Run the script
with sync_playwright() as playwright:
    run(playwright)
