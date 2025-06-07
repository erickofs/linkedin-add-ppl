import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BrowserManager:
    """Utility class to configure and start a Chrome WebDriver."""

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--log-level=3")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-popup-blocking")
        self.driver = None

    def choose_profile(self):
        """Ask the user for a Chrome profile and configure the options."""
        username = os.environ.get('USERNAME')
        user_data_dir = rf"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data"
        self.options.add_argument(f"--user-data-dir={user_data_dir}")
        profile_directory = input("\nEnter the Chrome profile directory name (press Enter for 'Default'): ").strip() or "Default"
        profile_path = os.path.join(user_data_dir, profile_directory)
        if not os.path.exists(profile_path):
            print(f"Profile '{profile_directory}' not found. Using 'Default' profile.")
            profile_directory = "Default"
        self.options.add_argument(f"--profile-directory={profile_directory}")
        print(f"Using Chrome profile: {profile_directory}\n")

    def start(self):
        """Launch Chrome with the configured options."""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        return self.driver
