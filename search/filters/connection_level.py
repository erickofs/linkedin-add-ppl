"""
Connection level filter for LinkedIn people search.
Applies 1st, 2nd, or 3rd+ connection degree filters.
"""

import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import random_delay, scroll_to_element


def apply_connection_level_filter(driver, levels):
    """
    Sets the connection level filters on the search results page.

    Args:
        driver: Selenium WebDriver instance.
        levels: List of connection levels (e.g. ['1st', '2nd', '3rd+']).
    """
    try:
        for lvl in levels:
            button_xpath = f"//button[@aria-label='{lvl}']"
            connection_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            scroll_to_element(driver, connection_button)

            aria_pressed = connection_button.get_attribute("aria-pressed")
            if aria_pressed == "false":
                connection_button.click()
                random_delay(0.5, 1)
                print(f"Connection level '{lvl}' selected.")
            else:
                print(f"Connection level '{lvl}' is already selected.")

    except Exception as e:
        print(f"Error setting connection levels: {e}")
        traceback.print_exc()
