from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException
import time

someone = '' #add someone's username whose followers you want to follow
username = '' #add your username
password = '' #add your password

chrome_options = Options()
driver = webdriver.Firefox(options=chrome_options)
driver.get(f"https://github.com/{someone}?tab=followers")

# Sign in
driver.find_element(By.CLASS_NAME, "HeaderMenu-link--sign-in").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#login_field").send_keys(f"{username}")
driver.find_element(By.ID, "password").send_keys(f"{password}")
driver.find_element(By.CSS_SELECTOR, value=".js-sign-in-button").click()
time.sleep(1)


def follow_users():
    # Find all 'Follow' buttons
    newlist = driver.find_elements(By.CSS_SELECTOR, "input[value='Follow']")

    for i in newlist:
        try:
            # Scroll the element into view
            driver.execute_script("arguments[0].scrollIntoView(true);", i)
            time.sleep(0.5)  # Adjust time if needed

            # Use JavaScript to click the button
            driver.execute_script("arguments[0].click();", i)
            time.sleep(0.05)  # Short pause between clicks

        except ElementNotInteractableException:
            print("Element not interactable. Skipping...")
        except TimeoutException:
            print("Timed out waiting for element to be clickable.")
        except Exception as e:
            print(f"An error occurred: {e}")


try:
    while True:
        follow_users()

        # Check for the presence of the 'Next' button
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination > a:nth-child(2)"))
        )

        if next_button:
            print("Clicking the 'Next' button.")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)  # Wait for the next page to load
        else:
            print("No 'Next' button found. Ending script.")
            break

except TimeoutException:
    print("No more pages left or 'Next' button not found.")
finally:
    driver.quit()
