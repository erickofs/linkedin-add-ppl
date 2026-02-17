"""
Company filter for LinkedIn people search.
Applies current company filters to narrow search results.
"""

import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import random_delay, scroll_to_element


def apply_company_filter(driver, companies):
    """
    Sets the company filters and clicks 'Show results'.

    Args:
        driver: Selenium WebDriver instance.
        companies: List of company names (e.g. ['Google', 'Microsoft']).
    """
    try:
        print("Attempting to locate the 'Companies' filter button...")
        company_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@aria-label='Current company filter. "
                    "Clicking this button displays all Current company filter options.']",
                )
            )
        )
        scroll_to_element(driver, company_filter)
        company_filter.click()
        random_delay(1, 2)

        for company in companies:
            print(f"Entering company: {company}")
            company_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@placeholder, 'Add a company')]")
                )
            )
            scroll_to_element(driver, company_input)
            company_input.clear()
            company_input.send_keys(company)
            random_delay(2, 4)

            try:
                company_option = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//li//span[text()='{company}']")
                    )
                )
                scroll_to_element(driver, company_option)
                company_option.click()
                random_delay(2, 4)
                print(f"Company '{company}' applied.")
            except Exception:
                print(
                    f"Company '{company}' not found in the dropdown. "
                    "Skipping to the next company."
                )
                continue

        # Click 'Show results' via the cancel button's sibling
        print("Attempting to locate the 'Cancel Companies filter' button...")
        cancel_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Cancel Current company filter']")
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
            print("Company filter applied successfully.\n")
        else:
            print(
                "The button following the 'Cancel' button does not have "
                "the expected text. Cannot proceed."
            )

    except Exception as e:
        print(f"Error setting company: {e}")
        traceback.print_exc()
        driver.save_screenshot("error_search_company.png")
