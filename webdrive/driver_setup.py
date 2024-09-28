import os
import time
import random
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class Chromedriver():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--log-level=3")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-popup-blocking")

    def start_browser(self):
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
            return self.driver
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            return None

def search_location(locations):
    """Sets the location filters and clicks the 'Show results' button relative to the 'Cancel Locations filter' button."""
    try:
        # Click on the 'Locations' filter using its unique ID
        print("Attempting to locate the 'Locations' filter button...")
        location_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "searchFilter_geoUrn"))
        )
        scroll_to_element(location_filter)
        location_filter.click()
        random_delay(1, 2)

        for loc in locations:
            # Enter the location
            print(f"Entering location: {loc}")
            location_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@placeholder, 'Add a location')]")
                )
            )
            scroll_to_element(location_input)
            location_input.clear()
            location_input.send_keys(loc)
            random_delay(1, 2)

            # Wait for the dropdown options to load and select the location
            location_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{loc}']"))
            )
            scroll_to_element(location_option)
            location_option.click()
            random_delay(1, 2)
            print(f"Location '{loc}' applied.")

         # Locate the 'Cancel Locations filter' button
        print("Attempting to locate the 'Cancel Locations filter' button...")
        cancel_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Cancel Locations filter']"))
        )
        scroll_to_element(cancel_button)

        # From the cancel button, find the next sibling button, which should be 'Show results'
        print("Locating the 'Show results' button relative to the 'Cancel' button...")
        apply_button_xpath = "./following-sibling::button[1]"
        apply_button = cancel_button.find_element(By.XPATH, apply_button_xpath)

        # Verify the button text to ensure it's the correct button
        button_text = apply_button.text.strip()
        if 'Show results' in button_text:
            print("Found the 'Show results' button. Attempting to click it...")
            scroll_to_element(apply_button)
            apply_button.click()
            random_delay(2, 3)
            print("Location filter applied successfully.\n")
        else:
            print("The button following the 'Cancel' button does not have the expected text. Cannot proceed.")

    except Exception as e:
        print(f"Error setting location: {e}")
        traceback.print_exc()
        driver.save_screenshot('error_search_location.png')

def search_company(companies):
    """Sets the company filters and clicks the 'Show results' button relative to the 'Cancel companies filter' button."""
    try:
        # Click on the 'Companies' filter using its unique ID
        print("Attempting to locate the 'Companies' filter button...")
        company_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Current company filter.']"))
        )
        scroll_to_element(company_filter)
        company_filter.click()
        random_delay(1, 2)

        for company in companies:
            # Enter the company
            print(f"Entering company: {company}")
            company_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@placeholder, 'Add a company')]")
                )
            )
            scroll_to_element(company_input)
            company_input.clear()
            company_input.send_keys(company)
            random_delay(1, 2)

            # Wait for the dropdown options to load and select the company
            company_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{company}']"))
            )
            scroll_to_element(company_option)
            company_option.click()
            random_delay(1, 2)
            print(f"Company '{company}' applied.")

        # Locate the 'Cancel Companies filter' button
        print("Attempting to locate the 'Cancel Companies filter' button...")
        cancel_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Cancel Current company filter']"))
        )
        scroll_to_element(cancel_button)

        # From the cancel button, find the next sibling button, which should be 'Show results'
        print("Locating the 'Show results' button relative to the 'Cancel' button...")
        apply_button_xpath = "./following-sibling::button[1]"
        apply_button = cancel_button.find_element(By.XPATH, apply_button_xpath)

        # Verify the button text to ensure it's the correct button
        button_text = apply_button.text.strip()
        if 'Show results' in button_text:
            print("Found the 'Show results' button. Attempting to click it...")
            scroll_to_element(apply_button)
            apply_button.click()
            random_delay(2, 3)
            print("Company filter applied successfully.\n")
        else:
            print("The button following the 'Cancel' button does not have the expected text. Cannot proceed.")

    except Exception as e:
        print(f"Error setting company: {e}")
        traceback.print_exc()
        driver.save_screenshot('error_search_company.png')
