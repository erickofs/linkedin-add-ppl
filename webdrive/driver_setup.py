"""
Chrome WebDriver setup and lifecycle management.
Handles browser initialization with user profile configuration.
"""

import os
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ChromeDriverSetup:
    """Manages Chrome WebDriver creation and teardown."""

    def __init__(self, profile_directory="Default"):
        """
        Configures Chrome options with the given user profile.

        Args:
            profile_directory: Chrome profile directory name (e.g. 'Default', 'Profile 1').
        """
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--log-level=3")
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-popup-blocking")

        # Configure user profile
        username = os.environ.get("USERNAME")
        if not username:
            raise EnvironmentError("Could not find the Windows USERNAME environment variable.")

        user_data_dir = rf"C:\Users\{username}\AppData\Local\Google\Chrome\User Data"

        # Validate profile directory
        profile_path = os.path.join(user_data_dir, profile_directory)
        if not os.path.exists(profile_path):
            print(f"Profile '{profile_directory}' not found. Using 'Default' profile.")
            profile_directory = "Default"

        print(f"Using Chrome profile: {profile_directory}\n")

        self.options.add_argument(f"--user-data-dir={user_data_dir}")
        self.options.add_argument(f"--profile-directory={profile_directory}")

        self.driver = None

    def start(self):
        """
        Starts the Chrome browser and returns the WebDriver instance.

        Returns:
            webdriver.Chrome instance, or None on failure.
        """
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=self.options,
            )
            print("Chrome browser started with user profile.\n")
            return self.driver
        except Exception as e:
            print(f"Error starting the browser: {e}")
            traceback.print_exc()
            return None

    def quit(self):
        """Closes the browser if it is open."""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")
