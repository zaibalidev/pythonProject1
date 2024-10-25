from asyncio import wait_for, timeout


from playwright_model import Util_playwright
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import sync_playwright
from credentials import user_name
import credentials




with sync_playwright() as playwright:

        #Launch a browser
        case_state=""
        case_priority=""
        case_subject_person=""
        case_ass_group=""
        #case_list=["HRC0000106","HRC0000126","Test123456","HRC0000167","HRC0000283"]
        case_list = ["HRC0000106"]
        browser=  playwright.chromium.launch(headless=False,slow_mo=1000)
        page= browser.new_page()



        url="https://net2appsdemo3.service-now.com/"
        page.goto(url)




        playwrightmodel= Util_playwright(page)
        # Search user_name and password
        txt_login=page.locator("id=user_name")
        txt_pwd=page.locator("id=user_password")

        # Fill username and password


        txt_login.fill(credentials.sn_user_name)
        txt_pwd.fill(credentials.sn_user_pwd)

        # Search login button and click
        #btn_login=page.get_by_role("button", name="Log in")
        #btn_login.click(
        if playwrightmodel.isElementsPresent("//button[text()='Log in']"):
                playwrightmodel.click_element("//button[text()='Log in']")

        user_list=["5656565","hr.agent","hr.agent.usa","hr.agent.france"]
        #playwrightmodel.repeatImpersonatedUsers(user_list, case_list, url)
        for impersonate_user in range(len(user_list)):
                if playwrightmodel.isImpersonated(user_list[impersonate_user]):
                        print("user found")
                        playwrightmodel.queryElementClick(f"seismic-hoist mark:text('{user_list[impersonate_user]}')")
                        playwrightmodel.queryElementClick("div.now-modal-footer button.now-button.-primary.-md")

                        page.wait_for_timeout(3000)
                        page.goto(
                                f"{url}sn_hr_core_case_list.do",
                                wait_until="domcontentloaded")
                        for case in range(len(case_list)):
                                print(case_list[case])
                                if playwrightmodel.isElementPresent("table#sn_hr_core_case_table thead"):
                                        thead = page.locator("table#sn_hr_core_case_table thead")
                                        thead.locator("//input[@aria-label='Search column: number']")
                                        txt_search_number = thead.locator("//input[@aria-label='Search column: number']")
                                        if txt_search_number.is_visible() != True:
                                                page.locator("th[name='search'] button").click()

                                        txt_search_number.fill(f"{case_list[case]}")

                                        page.press("//input[@aria-label='Search column: number']", "Enter")
                                        tbody = page.locator("table#sn_hr_core_case_table tbody")

                                        tr = tbody.locator("tr").first
                                        if tr.count() > 0:


                                                hrlink = f"//a[text()='{case_list[case]}']"
                                                if playwrightmodel.isElementPresent(hrlink, loca_type="xpath"):

                                                        playwrightmodel.click_element(hrlink, loca_type="xpath")
                                                        page.wait_for_timeout(1_000)
                                                        parsed_url = urlparse(page.url)
                                                        params = parse_qs(parsed_url.query)

                                                        # Extract the 'target' parameter value
                                                        target_value = parsed_url.path.split('/')[-1].split(".")[0]
                                                        print(target_value)

                                                        # Locate priority
                                                        priority_selected = page.locator(
                                                                "div.input_controls select[id*='priority'] option[selected='Selected']")
                                                        # Locate assignment group
                                                        ass_group = page.locator(
                                                                "div.input-group.ref-container input[id*='assignment_group']")

                                                        # Locate state
                                                        state_selected = page.locator(
                                                                "div.input_controls select[id*='state'] option[selected='selected']")
                                                        # Locate subject person
                                                        subject_person = page.locator(
                                                                "div.input-group.ref-container input[id*='subject_person34343']")

                                                        # check if above locators are found
                                                        if ass_group.count() > 0:
                                                                case_ass_group = ass_group.input_value()
                                                        else:
                                                                case_ass_group = "Element not found"
                                                        if subject_person.count() > 0:
                                                                case_subject_person = subject_person.input_value()
                                                        else:
                                                                case_subject_person = "Element not found"

                                                        if state_selected.count() > 0:
                                                                case_state = state_selected.inner_text()
                                                        else:
                                                                case_state = "Element not found"

                                                        if priority_selected.count() > 0:
                                                                case_priority = priority_selected.inner_text()
                                                        else:
                                                                case_priority = "Element not found"

                                                print(f"{case_priority} : {case_subject_person} : {ass_group.input_value()} : {case_state}")

                                                page.goto(
                                                        f"{url}sn_hr_core_case_list.do?sysparm_userpref_module=7a5330019f22120047a2d126c42e70e0&sysparm_query=active%3Dtrue%5EEQ&sysparm_clear_stack=true",
                                                        wait_until="domcontentloaded")
                                        else:
                                                print(f"Record Not Found:{case_list[case]}")

                else:
                        print("user not found")
                        page.goto(f"{url}/now/nav/ui/home",wait_until="domcontentloaded")
                page.goto(f"{url}/now/nav/ui/home")
        browser.close()




