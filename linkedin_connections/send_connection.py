"""
LinkedIn connection request sender.
Finds 'Connect' buttons on the search results page and sends invitations.
"""

import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import random_delay, scroll_to_element


def send_connection_requests(driver):
    """
    Sends connection requests to all visible results on the current page.

    Args:
        driver: Selenium WebDriver instance.
    """
    try:
        # Scroll to bottom to load all results
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_delay(2, 3)

        connections = driver.find_elements(
            By.XPATH, "//button[.//span[text()='Connect']]"
        )
        if not connections:
            print("No connect buttons found. Please check if there are available results.")
            return

        print(f"Found {len(connections)} connect button(s).")
        for index, connect_button in enumerate(connections):
            try:
                print(f"Sending connection request {index + 1} of {len(connections)}...")
                scroll_to_element(driver, connect_button)
                connect_button.click()
                random_delay(1, 2)

                send_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[span[text()='Send without a note']]")
                    )
                )
                send_button.click()
                random_delay(1, 2)
                print("Connection request sent successfully.")

            except Exception as e:
                print(f"Error sending connection: {e}")
                traceback.print_exc()
                # Close the popup if open
                try:
                    close_button = driver.find_element(
                        By.XPATH, "//button[@aria-label='Dismiss']"
                    )
                    close_button.click()
                    random_delay(0.5, 1)
                except Exception:
                    pass
                continue

    except Exception as e:
        print(f"Error sending connection requests: {e}")
        traceback.print_exc()
