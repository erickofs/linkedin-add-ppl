"""
Utility helper functions for browser automation.
Provides delay simulation and element scrolling.
"""

import time
import random


def random_delay(min_seconds=2, max_seconds=5):
    """Adds a random delay to simulate human behavior."""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Waiting for {round(delay, 2)} seconds...")
    time.sleep(delay)


def scroll_to_element(driver, element):
    """Scrolls the page to bring the element into view."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    random_delay(0.5, 1)
