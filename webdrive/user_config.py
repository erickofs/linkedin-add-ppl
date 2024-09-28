import os
from driver_setup import Chromedriver

class Chromeuserconfig():
    def __init__(self):
        self.options = Chromedriver.__init__(self).options
        self.username = os.environ.get('USERNAME')
        self.user_data_dir = rf"C:\Users\{self.username}\AppData\Local\Google\Chrome\User Data"
        self.profile_directory = input("\nEnter the Chrome profile directory name (press Enter for 'Default'): ").strip()
        
    def user_config(self):    
        self.options.add_argument(f"--user-data-dir={self.user_data_dir}")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--log-level=3")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-popup-blocking")
        self.user_data()
        return self.options
    
    def chrome_profile(self):
        """Chrome profile definition"""
        if not self.profile_directory:
            self.profile_directory = "Default"
        else:
            # Check if the profile directory exists
            profile_path = os.path.join(self.user_data_dir, self.profile_directory)
            if not os.path.exists(profile_path):
                print(f"Profile '{self.profile_directory}' not found. Using 'Default' profile.")
                self.profile_directory = "Default"
        print(f"Using Chrome profile: {self.profile_directory}\n")
        return self.profile_directory