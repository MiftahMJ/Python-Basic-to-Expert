from selenium.webdriver.common.by import By

def select_random_date(driver):
    """Select a random date for the calendar input."""
    from datetime import datetime
    import random

    start_date = datetime(1924, 1, 1)
    end_date = datetime(2004, 12, 31)
    random_date = start_date + (end_date - start_date) * random.random()
    random_date_str = random_date.strftime("%d.%m.%Y")

    date_input = driver.find_element(By.ID, "fields1content")
    driver.execute_script(f"arguments[0].value = '{random_date_str}';", date_input)
    print(f"Random date selected: {random_date_str}")

def fill_form(driver):
    """Fill the form on the third page."""
    try:
        driver.find_element(By.ID, "appointment_newAppointmentForm_lastname").send_keys("Doe")
        driver.find_element(By.ID, "appointment_newAppointmentForm_firstname").send_keys("John")
        driver.find_element(By.ID, "appointment_newAppointmentForm_email").send_keys("john.doe@example.com")
        driver.find_element(By.ID, "appointment_newAppointmentForm_emailrepeat").send_keys("john.doe@example.com")
        driver.find_element(By.ID, "appointment_newAppointmentForm_fields_0__content").send_keys("A12345678")

        select_random_date(driver)

        driver.find_element(By.ID, "appointment_newAppointmentForm_fields_2__content").click()  # Checkbox
        driver.find_element(By.ID, "appointment_newAppointmentForm_fields_3__content").send_keys("1234567890")
        driver.find_element(By.ID, "appointment_newAppointmentForm_fields_4__content").send_keys("Example University")
    except Exception as e:
        print(f"Error while filling the form: {e}")
