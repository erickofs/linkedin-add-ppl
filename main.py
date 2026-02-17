"""
LinkedIn People Connector — Main Orchestrator.
Automates sending connection requests on LinkedIn based on search criteria.

Usage:
    python main.py
"""

import time

from utils.user_input import (
    chrome_profile_input,
    search_term_input,
    conn_level_input,
    location_input,
    company_input,
    pages_input,
)
from webdrive.driver_setup import ChromeDriverSetup
from search.people_search import search_people
from search.pagination import go_to_next_page
from search.filters.connection_level import apply_connection_level_filter
from search.filters.location import apply_location_filter
from search.filters.company import apply_company_filter
from linkedin_connections.send_connection import send_connection_requests


def main():
    """Main entry point — collects inputs, starts browser, runs automation."""

    # 1. Collect all user inputs upfront
    profile_directory = chrome_profile_input()
    search_term = search_term_input()
    levels = conn_level_input()
    locations = location_input()
    companies = company_input()
    pages_to_navigate = pages_input()

    # 2. Start the browser
    browser = ChromeDriverSetup(profile_directory)
    driver = browser.start()
    if not driver:
        print("Failed to start the browser. Exiting.")
        return

    time.sleep(5)  # Wait for browser to fully load

    # 3. Search and apply filters
    search_people(driver, search_term)
    apply_connection_level_filter(driver, levels)
    apply_location_filter(driver, locations)
    apply_company_filter(driver, companies)

    # 4. Iterate through pages and send connection requests
    for _ in range(pages_to_navigate):
        send_connection_requests(driver)
        if not go_to_next_page(driver):
            break

    # 5. Ask if user wants to close the browser
    close = input("Do you want to close the browser? (y/n): ").strip().lower()
    if close == "y":
        browser.quit()
    else:
        print("Leaving the browser open.")


if __name__ == "__main__":
    main()
