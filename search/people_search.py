"""
LinkedIn people search functionality.
Navigates to LinkedIn and performs a people search by keyword.
"""

import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import random_delay, scroll_to_element


def search_people(driver, search_term):
    """
    Searches for people on LinkedIn based on the provided search term.

    Args:
        driver: Selenium WebDriver instance.
        search_term: Keyword to search for.
    """
    driver.get("https://www.linkedin.com/feed/")
    try:
        print("Attempting to locate the search box...")
        search_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[contains(@placeholder, 'Search')]")
            )
        )
        search_box.clear()
        print("Search box found, entering search term...")
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        random_delay(3, 5)

        print("Search results page loaded successfully.")

        # Click on the 'People' filter
        print("Attempting to locate the 'People' filter button...")
        people_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'search-reusables__filter-pill') and text()='People']",
                )
            )
        )
        scroll_to_element(driver, people_filter)
        print("Clicking the 'People' filter button...")
        people_filter.click()
        random_delay(2, 4)
        print(f"Search for '{search_term}' completed.\n")

    except Exception as e:
        print(f"Error during search: {e}")
        traceback.print_exc()
        driver.save_screenshot("error_search_people.png")
