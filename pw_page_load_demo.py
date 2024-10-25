from playwright.sync_api import sync_playwright
from time import perf_counter
with sync_playwright() as playwright:

    browser=playwright.chromium.launch(headless=False,slow_mo=500)
    page=browser.new_page()
    print("Page loading...")
    start=perf_counter()
    #wait_until values are load,networkdidele,commit
    page.goto("https://www.scrapethissite.com/pages/ajax-javascript/", wait_until="domcontentloaded",timeout=4_500)
    link= page.get_by_role("link",name="2015")
    link.click()


    element=page.locator("td.film-title").first
    #page.wait_for_selector(selector="td.film-title")
    element.wait_for()
    time_taken =perf_counter()-start_time
    print(f"movies are loaded, in {round(time_taken,2)}s!")
    browser.close()

   # time_taken=perf_counter()-start
    #url="https://www.scrapethissite.com/pages/ajax-javascript/"
    #print(f"..Page loaded in {round(time_taken,2)}s")
    #browser.close()