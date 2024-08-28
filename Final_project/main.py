from driver import init_driver
from captcha_solver import capture_captcha_image, solve_captcha
from form_filler import fill_form
from utils import scroll_to_element

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def main():
    # Read URL from file
    with open("urls.txt", "r") as file:
        first_url = file.readline().strip()

    driver = init_driver()
    driver.get(first_url)

    try:
        # Wait for the first page to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print("First page loaded successfully.")

        # Solve CAPTCHA on the first page
        captcha_base64 = capture_captcha_image(driver)
        captcha_solution = solve_captcha(captcha_base64)
        if captcha_solution:
            try:
                captcha_input = driver.find_element(By.ID, "appointment_captcha_day_captchaText")
                captcha_input.clear()
                captcha_input.send_keys(captcha_solution)

                submit_button = driver.find_element(By.ID, "appointment_captcha_day_appointment_showDay")
                submit_button.click()
                print("First page CAPTCHA solved and form submitted.")

                # Wait for the second page to load
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                print("Second page loaded successfully.")

                # Attempt to find the "Book Appointment" button
                try:
                    # Adding wait to ensure the element is present and clickable
                    book_appointment_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'appointment_showForm')]"))
                    )
                    book_appointment_button.click()
                    print("Navigated to the third page.")
                except TimeoutException:
                    print("Book Appointment button not found after waiting. Printing page source for debugging.")
                    print(driver.page_source)  # Debug: Print the page source
                    return

                # Wait for the third page to load
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                print("Third page loaded successfully.")

                fill_form(driver)
                print("Form filled successfully.")

                # Scroll to CAPTCHA image and solve it
                captcha_image_element = driver.find_element(By.XPATH, "//captcha/div[contains(@style, 'background')]")
                scroll_to_element(driver, captcha_image_element)
                third_captcha_base64 = capture_captcha_image(driver)
                third_captcha_solution = solve_captcha(third_captcha_base64)

                if third_captcha_solution:
                    print(f"Third page CAPTCHA solved: {third_captcha_solution}")
                    captcha_input = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.ID, "appointment_newAppointmentForm_captchaText"))
                    )
                    scroll_to_element(driver, captcha_input)
                    captcha_input.clear()
                    captcha_input.send_keys(third_captcha_solution)
                    print("CAPTCHA entered on third page.")
                    # Uncomment the next line to submit the form automatically
                    # driver.find_element(By.ID, "appointment_newAppointmentForm_appointment_addAppointment").click()

            except NoSuchElementException as e:
                print(f"Error finding input field or submit button: {e}")
            except Exception as e:
                print(f"Error during form submission: {e}")

    except TimeoutException as e:
        print(f"Error: Page did not load within the expected time: {e}")

    driver.quit()


if __name__ == "__main__":
    main()
