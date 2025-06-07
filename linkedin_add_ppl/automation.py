import os
import random
import time
import traceback
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def random_delay(min_seconds: float = 2, max_seconds: float = 5) -> None:
    """Sleep for a random time between the given limits."""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Waiting for {round(delay, 2)} seconds...")
    time.sleep(delay)


def scroll_to_element(driver, element) -> None:
    """Scroll the page to bring the element into view."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    random_delay(0.5, 1)


def pages_input() -> int:
    pages = input("Enter the number of pages to navigate (default is 3): ")
    return int(pages) if pages.isdigit() else 3


def search_term_input() -> str:
    return input("Enter the search term to find people on LinkedIn: ")


def conn_level_input() -> List[str]:
    level_list = []
    while not level_list:
        lvl_input = input("Enter the connection levels to search for, separated by commas (1, 2, 3): ")
        lvl_input = lvl_input.replace(" ", "")
        valid_levels = {'1': '1st', '2': '2nd', '3': '3rd+'}
        levels = lvl_input.split(",")
        for level in levels:
            if level in valid_levels:
                level_list.append(valid_levels[level])
            else:
                print(f"Invalid connection level: {level}. Please enter 1, 2, or 3.")
                level_list = []
                break
    print(f"Connection levels to be searched: {level_list}\n")
    return level_list


def conn_level(driver, levels: List[str]) -> None:
    try:
        for lvl in levels:
            button_xpath = f"//button[@aria-label='{lvl}']"
            connection_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            scroll_to_element(driver, connection_button)
            if connection_button.get_attribute('aria-pressed') == 'false':
                connection_button.click()
                random_delay(0.5, 1)
                print(f"Connection level '{lvl}' selected.")
            else:
                print(f"Connection level '{lvl}' is already selected.")
    except Exception as exc:
        print(f"Error setting connection levels: {exc}")
        traceback.print_exc()


def search_people(driver, search_term: str) -> None:
    driver.get("https://www.linkedin.com/feed/")
    try:
        search_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'Search')]"))
        )
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        random_delay(3, 5)
        people_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'search-reusables__filter-pill') and text()='People']")
            )
        )
        scroll_to_element(driver, people_filter)
        people_filter.click()
        random_delay(2, 4)
        print(f"Search for '{search_term}' completed.\n")
    except Exception as exc:
        print(f"Error during search: {exc}")
        traceback.print_exc()
        driver.save_screenshot('error_search_people.png')


def location_input() -> List[str]:
    location_list = []
    while not location_list:
        location_input = input("Enter the locations to search for, separated by commas: ")
        location_list = [loc.strip() for loc in location_input.split(',') if loc.strip()]
        location_list = random.sample(location_list, len(location_list))
        if not location_list:
            print("Please enter at least one valid location.")
    print(f"Locations to be searched: {location_list}\n")
    return location_list


def search_location(driver, locations: List[str]) -> None:
    try:
        location_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "searchFilter_geoUrn"))
        )
        scroll_to_element(driver, location_filter)
        location_filter.click()
        random_delay(1, 2)
        for loc in locations:
            location_input_el = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'Add a location')]"))
            )
            scroll_to_element(driver, location_input_el)
            location_input_el.clear()
            location_input_el.send_keys(loc)
            random_delay(1, 2)
            location_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{loc}']"))
            )
            scroll_to_element(driver, location_option)
            location_option.click()
            random_delay(1, 2)
            print(f"Location '{loc}' applied.")
        cancel_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Cancel Locations filter']"))
        )
        scroll_to_element(driver, cancel_button)
        apply_button = cancel_button.find_element(By.XPATH, "./following-sibling::button[1]")
        if 'Show results' in apply_button.text.strip():
            scroll_to_element(driver, apply_button)
            apply_button.click()
            random_delay(2, 3)
            print("Location filter applied successfully.\n")
    except Exception as exc:
        print(f"Error setting location: {exc}")
        traceback.print_exc()
        driver.save_screenshot('error_search_location.png')


def company_input() -> List[str]:
    company_list = []
    while not company_list:
        company_input_val = input("Enter the companies to search for, separated by commas: ")
        company_list = [comp.strip() for comp in company_input_val.split(',') if comp.strip()]
        company_list = random.sample(company_list, len(company_list))
        if not company_list:
            print("Please enter at least one valid company.")
    print(f"Companies to be searched: {company_list}\n")
    return company_list


def search_company(driver, companies: List[str]) -> None:
    try:
        company_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Current company filter. Clicking this button displays all Current company filter options.']"))
        )
        scroll_to_element(driver, company_filter)
        company_filter.click()
        random_delay(1, 2)
        for company in companies:
            company_input_el = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'Add a company')]"))
            )
            scroll_to_element(driver, company_input_el)
            company_input_el.clear()
            company_input_el.send_keys(company)
            random_delay(2, 4)
            try:
                company_option = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{company}']"))
                )
                scroll_to_element(driver, company_option)
                company_option.click()
                random_delay(2, 4)
                print(f"Company '{company}' applied.")
            except Exception:
                print(f"Company '{company}' not found in the dropdown. Skipping to the next company.")
                continue
        cancel_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Cancel Current company filter']"))
        )
        scroll_to_element(driver, cancel_button)
        apply_button = cancel_button.find_element(By.XPATH, "./following-sibling::button[1]")
        if 'Show results' in apply_button.text.strip():
            scroll_to_element(driver, apply_button)
            apply_button.click()
            random_delay(2, 3)
            print("Company filter applied successfully.\n")
    except Exception as exc:
        print(f"Error setting company: {exc}")
        traceback.print_exc()
        driver.save_screenshot('error_search_company.png')


def send_connection_requests(driver) -> None:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_delay(2, 3)
        connections = driver.find_elements(By.XPATH, "//button[.//span[text()='Connect']]")
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
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Send without a note']]"))
                )
                send_button.click()
                random_delay(1, 2)
                print("Connection request sent successfully.")
            except Exception as exc:
                print(f"Error sending connection: {exc}")
                traceback.print_exc()
                try:
                    close_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                    close_button.click()
                    random_delay(0.5, 1)
                except Exception:
                    pass
                continue
    except Exception as exc:
        print(f"Error sending connection requests: {exc}")
        traceback.print_exc()


def go_to_next_page(driver) -> bool:
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Next')]"))
        )
        scroll_to_element(driver, next_button)
        next_button.click()
        random_delay(2, 4)
        print("Navigating to the next page.")
        return True
    except Exception as exc:
        print(f"Error navigating to the next page: {exc}")
        traceback.print_exc()
        return False


def run(driver) -> None:
    """Execute the whole automation flow using the provided driver."""
    search_term = search_term_input()
    levels = conn_level_input()
    locations = location_input()
    companies = company_input()
    pages_to_navigate = pages_input()

    search_people(driver, search_term)
    conn_level(driver, levels)
    search_location(driver, locations)
    search_company(driver, companies)

    for _ in range(pages_to_navigate):
        send_connection_requests(driver)
        if not go_to_next_page(driver):
            break
