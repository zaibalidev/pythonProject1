from playwright.sync_api import  sync_playwright
def on_download(download):
    print("event listner is fired")
    download.save_as("night1.jpg")
with sync_playwright() as playwright:
    browser=playwright.chromium.launch(headless=False,slow_mo=1000)
    page=browser.new_page()
    page.goto("https://unsplash.com/photos/qe2RkzzMx9A")
    #btn=page.get_by_role("link",name='Download free')
    page.once("download",on_download)
    page.locator("//button[@title='Choose your download size']").click()
    btn= page.get_by_role("link", name="Small (640 x 853)")
    btn.click()


    #with page.expect_download() as download_info:
     #   btn.click()
    #download=download_info.value
    #download.save_as("moon.jpg")
    #browser.close()
