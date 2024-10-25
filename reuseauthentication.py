
from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    browser= playwright.firefox.launch(headless=False, slow_mo=500)
    ctx=browser.new_context(
        storage_state="playwright/.auth/storage_stage.json"
    )

    page=ctx.new_page()
    page.goto("https://accounts.google.com")
    page.close()

    # save authentication state

    ctx.close()







