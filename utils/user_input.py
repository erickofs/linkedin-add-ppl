"""
CLI user input functions.
Collects and validates all user inputs before automation begins.
"""

import random


def search_term_input():
    """Prompts the user for the search term."""
    search_term = input("Enter the search term to find people on LinkedIn: ")
    return search_term


def conn_level_input():
    """Prompts the user for desired connection levels."""
    level_list = []
    while not level_list:
        lvl_input = input(
            "Enter the connection levels to search for, separated by commas (1, 2, 3): "
        )
        lvl_input = lvl_input.replace(" ", "")
        valid_levels = {"1": "1st", "2": "2nd", "3": "3rd+"}
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


def location_input():
    """Prompts the user for desired locations."""
    location_list = []
    while not location_list:
        loc_input = input("Enter the locations to search for, separated by commas: ")
        location_list = [loc.strip() for loc in loc_input.split(",") if loc.strip()]
        location_list = random.sample(location_list, len(location_list))
        if not location_list:
            print("Please enter at least one valid location.")
    print(f"Locations to be searched: {location_list}\n")
    return location_list


def company_input():
    """Prompts the user for desired companies."""
    company_list = []
    while not company_list:
        comp_input = input("Enter the companies to search for, separated by commas: ")
        company_list = [comp.strip() for comp in comp_input.split(",") if comp.strip()]
        company_list = random.sample(company_list, len(company_list))
        if not company_list:
            print("Please enter at least one valid company.")
    print(f"Companies to be searched: {company_list}\n")
    return company_list


def pages_input():
    """Prompts the user for the number of pages to navigate."""
    pages = input("Enter the number of pages to navigate (default is 3): ")
    if pages.isdigit():
        return int(pages)
    return 3


def chrome_profile_input():
    """Prompts the user for the Chrome profile directory name."""
    profile_directory = input(
        "\nEnter the Chrome profile directory name (press Enter for 'Default'): "
    ).strip()
    if not profile_directory:
        profile_directory = "Default"
    return profile_directory
