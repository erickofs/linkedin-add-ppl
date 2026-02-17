"""
Location filter for LinkedIn people search.
Applies geographic location filters to narrow search results.
"""

import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import random_delay, scroll_to_element


def apply_location_filter(driver, locations):
    """
    Sets the location filters and clicks 'Show results'.

    Args:
        driver: Selenium WebDriver instance.
        locations: List of location names (e.g. ['São Paulo', 'New York']).
    """
    try:
        print("Attempting to locate the 'Locations' filter button...")
        location_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "searchFilter_geoUrn"))
        )
        scroll_to_element(driver, location_filter)
        location_filter.click()
        random_delay(1, 2)

        for loc in locations:
            print(f"Entering location: {loc}")
            location_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@placeholder, 'Add a location')]")
                )
            )
            scroll_to_element(driver, location_input)
            location_input.clear()
            location_input.send_keys(loc)
            random_delay(1, 2)

            location_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//li//span[text()='{loc}']")
                )
            )
            scroll_to_element(driver, location_option)
            location_option.click()
            random_delay(1, 2)
            print(f"Location '{loc}' applied.")

        # Click 'Show results' via the cancel button's sibling
        print("Attempting to locate the 'Cancel Locations filter' button...")
        cancel_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Cancel Locations filter']")
            )
        )
        scroll_to_element(driver, cancel_button)

        apply_button = cancel_button.find_element(
            By.XPATH, "./following-sibling::button[1]"
        )
        button_text = apply_button.text.strip()

        if "Show results" in button_text:
            print("Found the 'Show results' button. Attempting to click it...")
            scroll_to_element(driver, apply_button)
            apply_button.click()
            random_delay(2, 3)
            print("Location filter applied successfully.\n")
        else:
            print(
                "The button following the 'Cancel' button does not have "
                "the expected text. Cannot proceed."
            )

    except Exception as e:
        print(f"Error setting location: {e}")
        traceback.print_exc()
        driver.save_screenshot("error_search_location.png")
