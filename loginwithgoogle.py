
from credentials import user_name,pwd
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser =playwright.chromium.launch(headless=False,slow_mo=500)
    page=browser.new_page()
    page.goto("http://accounts.google.com")
    page.get_by_label("Email or phone").fill(user_name)
    page.get_by_role("button",name="Next").click()

    page.get_by_label("Enter your password").fill(pwd)
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Google apps").first.click()
    page.frame_locator("iframe")
    iframe=page.frame(name="app")
    iframe.locator("//a[@aria-label='Gmail, row 1 of 4 and column 3 of 3 in the first section (opens a new tab)']").click()


