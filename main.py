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

def choose_chrome_profile(user_data_dir):
    """Prompts the user to choose a Chrome profile."""
    profiles = [name for name in os.listdir(user_data_dir) if os.path.isdir(os.path.join(user_data_dir, name))]
    print("\nAvailable Chrome profiles:")
    for profile in profiles:
        print(f"- {profile}")
    profile_directory = input("\nEnter the Chrome profile directory name (press Enter for 'Default'): ").strip()
    if not profile_directory:
        profile_directory = "Default"
    else:
        # Check if the profile directory exists
        profile_path = os.path.join(user_data_dir, profile_directory)
        if not os.path.exists(profile_path):
            print(f"Profile '{profile_directory}' not found. Using 'Default' profile.")
            profile_directory = "Default"
    print(f"Using Chrome profile: {profile_directory}\n")
    return profile_directory

def pages_input():
    """Prompts the user for the number of pages to navigate."""
    pages = input("Enter the number of pages to navigate (default is 3): ")
    if pages.isdigit():
        return int(pages)
    else:
        return 3

def search_term_input():
    """Prompts the user for the search term."""
    search_term = input("Enter the search term to find people on LinkedIn: ")
    return search_term

def random_delay(min_seconds=2, max_seconds=5):
    """Adds a random delay to simulate human behavior."""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Waiting for {round(delay, 2)} seconds...")
    time.sleep(delay)

def scroll_to_element(element):
    """Scrolls the page to bring the element into view."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    random_delay(0.5, 1)

def conn_level_input():
    """Prompts the user for desired connection levels."""
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

def conn_level(levels):
    """Sets the connection level filters."""
    try:
        for lvl in levels:
            # Locate the button for the specific connection level
            button_xpath = f"//button[@aria-label='{lvl}']"
            connection_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            scroll_to_element(connection_button)

            # Check if the button is already selected
            aria_pressed = connection_button.get_attribute('aria-pressed')
            if aria_pressed == 'false':
                connection_button.click()
                random_delay(0.5, 1)
                print(f"Connection level '{lvl}' selected.")
            else:
                print(f"Connection level '{lvl}' is already selected.")
    except Exception as e:
        print(f"Error setting connection levels: {e}")
        traceback.print_exc()

def search_people(search_term):
    """Searches for people on LinkedIn based on the provided search term."""
    # Navigate to the LinkedIn homepage
    driver.get("https://www.linkedin.com/feed/")
    try:
        # Find the search box and enter the search term
        print("Attempting to locate the search box...")
        search_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'Search')]"))
        )
        search_box.clear()
        print("Search box found, entering search term...")
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        random_delay(3, 5)
        # Wait for the search results page to load
        print("Search results page loaded successfully.")


       # Click on the 'People' filter
        print("Attempting to locate the 'People' filter button...")
        people_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'search-reusables__filter-pill') and text()='People']")
            )
        )
        scroll_to_element(people_filter)
        print("Clicking the 'People' filter button...")
        people_filter.click()
        random_delay(2, 4)
        print(f"Search for '{search_term}' completed.\n")
    except Exception as e:
        print(f"Error during search: {e}")
        traceback.print_exc()
        driver.save_screenshot('error_search_people.png')


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


def send_connection_requests():
    """Sends connection requests to all the search results that meet the criteria."""
    try:
        # Scroll to the bottom to load all results
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_delay(2, 3)

        # Find all 'Connect' buttons
        connections = driver.find_elements(By.XPATH, "//button[.//span[text()='Connect']]")
        if not connections:
            print("No connect buttons found. Please check if there are available results.")
            return

        print(f"Found {len(connections)} connect button(s).")
        for index, connect_button in enumerate(connections):
            try:
                print(f"Sending connection request {index + 1} of {len(connections)}...")
                scroll_to_element(connect_button)
                connect_button.click()
                random_delay(1, 2)

                # Click on 'Send now' button in the popup
                send_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Send without a note']]"))
                )
                send_button.click()
                random_delay(1, 2)
                print("Connection request sent successfully.")
            except Exception as e:
                print(f"Error sending connection: {e}")
                traceback.print_exc()
                # Close the popup if open
                try:
                    close_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                    close_button.click()
                    random_delay(0.5, 1)
                except:
                    pass
                continue
    except Exception as e:
        print(f"Error sending connection requests: {e}")
        traceback.print_exc()

def go_to_next_page():
    """Navigates to the next page of results."""
    try:
        # Find the 'Next' button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Next')]"))
        )
        scroll_to_element(next_button)
        next_button.click()
        random_delay(2, 4)
        print("Navigating to the next page.")
        return True
    except Exception as e:
        print(f"Error navigating to the next page: {e}")
        traceback.print_exc()
        return False

def location_input():
    """Prompts the user for desired locations."""
    location_list = []
    while not location_list:
        location_input = input("Enter the locations to search for, separated by commas: ")
        location_list = [loc.strip() for loc in location_input.split(",") if loc.strip()]
        location_list = random.sample(location_list, len(location_list))
        if not location_list:
            print("Please enter at least one valid location.")
    print(f"Locations to be searched: {location_list}\n")
    return location_list

def company_input():
    """Prompts the user for desired locations."""
    company_list = []
    while not company_list:
        company_input = input("Enter the companies to search for, separated by commas: ")
        # Randomize the order of companies
        company_list = [comp.strip() for comp in company_input.split(",") if comp.strip()]
        company_list = random.sample(company_list, len(company_list))
        if not company_list:
            print("Please enter at least one valid company.")
    print(f"Companies to be searched: {company_list}\n")
    return company_list

def search_company(companies):
    """Sets the company filters and clicks the 'Show results' button relative to the 'Cancel companies filter' button."""
    try:
        # Click on the 'Companies' filter using its unique ID
        print("Attempting to locate the 'Companies' filter button...")
        company_filter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Current company filter. Clicking this button displays all Current company filter options.']"))
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
            random_delay(2, 4)

            # Wait for the dropdown options to load and select the company
            # If the exact company name is not found, skip to the next company
            try:
                company_option = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{company}']"))
                )
                scroll_to_element(company_option)
                company_option.click()
                random_delay(2, 4)
                print(f"Company '{company}' applied.")
            except Exception as e:
                print(f"Company '{company}' not found in the dropdown. Skipping to the next company.")
                continue

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

# Main execution
if __name__ == "__main__":
    # Initialize the WebDriver to open a new Chrome browser instance
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--disable-extensions")

    # Automatically find the Windows username
    username = os.environ.get('USERNAME')
    if not username:
        print("Could not find the Windows username.")


    # Construct the path to the Chrome user data directory
    user_data_dir = rf"C:\Users\{username}\AppData\Local\Google\Chrome\User Data"
    options.add_argument(f"--user-data-dir={user_data_dir}")

    def choose_chrome_profile(user_data_dir):
        """Prompts the user to choose a Chrome profile."""
        profile_directory = input("\nEnter the Chrome profile directory name (press Enter for 'Default'): ").strip()
        if not profile_directory:
            profile_directory = "Default"
        else:
            # Check if the profile directory exists
            profile_path = os.path.join(user_data_dir, profile_directory)
            if not os.path.exists(profile_path):
                print(f"Profile '{profile_directory}' not found. Using 'Default' profile.")
                profile_directory = "Default"
        print(f"Using Chrome profile: {profile_directory}\n")
        return profile_directory

    # Prompt the user to choose a Chrome profile
    profile_directory = choose_chrome_profile(user_data_dir)
    options.add_argument(f"--profile-directory={profile_directory}")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("Chrome browser started with user profile.\n")
    except Exception as e:
        print(f"Error starting the browser: {e}")


    # Wait for the browser to load
    time.sleep(5)

    # Prompt for user inputs
    search_term = search_term_input()
    levels = conn_level_input()
    locations = location_input()
    companies = company_input()
    pages_to_navigate = pages_input()

    search_people(search_term)
    conn_level(levels)
    search_location(locations)
    search_company(companies)

    # Loop through the specified number of pages
    for _ in range(pages_to_navigate):
        send_connection_requests()
        if not go_to_next_page():
            break

    # Ask if user wants to close the browser
    random_delay(2, 4)
    close_browser = input("Do you want to close the browser? (y/n): ").strip().lower()
    if close_browser == 'y':
        driver.quit()
        print("Browser closed.")
    else:
        print("Leaving the browser open.")

