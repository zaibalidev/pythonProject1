import time

from playwright_model import Util_playwright

from playwright.sync_api import sync_playwright
from credentials import sn_user_name, sn_user_pwd
import credentials
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

with sync_playwright() as p:
    objRecords=[
        {"user":"Zaib","art":"KBC100"}]
    user_list=["hr.agent.usa","abel.tuter","3433434343"]
    articles_list=["KB0000028","KB0000025"]
    browser = p.chromium.launch(headless=False,slow_mo=800)
   # context = browser.new_context(
   #     record_video_dir="videos/",  # Directory to save the recorded video
    #    record_video_size={"width": 1280, "height": 720}  # Set desired video resolution
    #)

    # page = context.new_page()
    page=browser.new_page()
    url = "https://net2appsdemo3.service-now.com/"
    try:
        page.goto(url)
        playwrightmodel = Util_playwright(page)
        playwrightmodel.serviceNowLogin(sn_user_name,sn_user_pwd)
        page.wait_for_timeout(10000)
        for impersonate_user in range(len(user_list)):
            if playwrightmodel.isImpersonated(user_list[impersonate_user]):

                strPrint=f"//seismic-hoist mark:text('{user_list[impersonate_user]}')"

                print(playwrightmodel.xpath_to_css(strPrint))
                playwrightmodel.click_element(locator=strPrint,loca_type="cspath")
                playwrightmodel.click_element(locator=f"//div[@class='now-modal-footer']//button[@class='now-button']//span:text('Impersonate user')",loca_type="cspath")
                playwrightmodel.isQueryElementPresent(playwrightmodel.xpath_to_css("//sn-polaris-header//div[@class='polaris-header-logo']"),_timeout=5000)


                for anumber in range(len(articles_list)):
                    page.goto(f"{url}esc?id=kb_article&sysparm_article={articles_list[anumber]}",wait_until="load")

                    if playwrightmodel.isElementPresent(locator="//h1[contains(@class,'widget-header')]"):

                        print(f"{user_list[impersonate_user]} can view arcticle: {articles_list[anumber]}")

                    else:
                        print("user has no permissions")
                    # playwrightmodel.take_screenshot_and_save(folder_path="./screenshots",file_name=f"{articles_list[anumber]}_{user_list[impersonate_user]}.png")
                    page.goto(f"{url}/now/nav/ui/home",wait_until="load")
            else:
                print(f"user not found {user_list[impersonate_user]}")
                page.get_by_role("button",name="Cancel").click()
                playwrightmodel.snImpersonatedUser(user_list[impersonate_user])
                # page.goto(f"{url}/now/nav/ui/home")
    except PlaywrightTimeoutError:
        print("Playwright timeout error")

    browser.close()



