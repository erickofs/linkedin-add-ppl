from linkedin_add_ppl.browser import BrowserManager
from linkedin_add_ppl import automation


def main() -> None:
    browser = BrowserManager()
    browser.choose_profile()
    driver = browser.start()

    automation.run(driver)

    close_browser = input("Do you want to close the browser? (y/n): ").strip().lower()
    if close_browser == 'y':
        driver.quit()
        print("Browser closed.")
    else:
        print("Leaving the browser open.")


if __name__ == "__main__":
    main()
