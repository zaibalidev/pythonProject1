from playwright.sync_api import sync_playwright
from time import perf_counter

def on_dialog(dialog):
    print("dialog opened:", dialog)
    dialog.accept()


with sync_playwright() as playwright:
    browser= playwright.chromium.launch(headless=False,slow_mo=1000)
    page=browser.new_page()
    page.goto("https://testpages.herokuapp.com/styled/alerts/alert-test.html")
    page.on("dialog", on_dialog)
    alert_btn= page.get_by_text("show confirm box")
    alert_btn.click()
    browser.close()


