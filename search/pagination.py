"""
Search results pagination.
Handles navigation between pages of LinkedIn search results.
"""

import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import random_delay, scroll_to_element


def go_to_next_page(driver):
    """
    Navigates to the next page of search results.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        True if navigation succeeded, False otherwise.
    """
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, 'Next')]")
            )
        )
        scroll_to_element(driver, next_button)
        next_button.click()
        random_delay(2, 4)
        print("Navigating to the next page.")
        return True
    except Exception as e:
        print(f"Error navigating to the next page: {e}")
        traceback.print_exc()
        return False
