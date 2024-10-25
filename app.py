from asyncio import timeout

from playwright.sync_api import sync_playwright
from credentials import user_name,pwd


with (sync_playwright() as playwright):
        browser=playwright.firefox.launch(headless=False,slow_mo=800)
        ctx=  browser.new_context(storage_state="playwright/.auth/storage_stage.json")
        page=ctx.new_page()
        page.goto("https://gmail.com")
        table=page.locator("div.UI table")
        email_rows= table.locator("tr").all()
        new_emails=[]
        for row in email_rows:
                #r=email_rows.nth(row)
                list_element=row.locator("//li[@data-tooltip='Mark as read']")

                if list_element.count()>0 :

                        name=""
                        emails=row.locator("td span[email]:visible")
                        for n in range (emails.count()):
                                if n==0:
                                        name=name+""+  emails.nth(n).inner_text()
                                else:
                                        name=name+","+  emails.nth(n).inner_text()

                        des = row.locator("td span[data-thread-id]:visible").inner_text()
                        new_emails.append([name,des])
                        #print(f"{name} - {des}")
        for new_email in new_emails:
                print(new_email[0],new_email[1])
                print("-"*20)

        ctx.close()






