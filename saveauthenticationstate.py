
from playwright.sync_api import sync_playwright
from credentials import user_name,pwd

with sync_playwright() as playwright:
    browser= playwright.firefox.launch(headless=False, slow_mo=500)
    ctx=browser.new_context()

    page=ctx.new_page()
    page.goto("https://accounts.google.com")

    txtEmail=page.get_by_label("Email or phone")
    txtEmail.fill(user_name)

    button=page.get_by_role("button", name="Next")
    button.click()
    txtEmail = page.get_by_label("Enter your password")
    txtEmail.fill(pwd)

    button1 = page.get_by_role("button", name="Next")
    button1.click()
    page.pause()

    # save authentication state
    ctx.storage_state(
        path="playwright/.auth/storage_stage.json"
    )
    ctx.close()







