from asyncio import wait_for


import re
import playwright.sync_api
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from urllib3.util.wait import select_wait_for_socket
from urllib.parse import urlparse, parse_qs
from Util_Wait import *
from credentials import user_name
import credentials
import os


class Util_playwright():
    def __init__(self, page: playwright.sync_api.Page):
        self.page = page

    def isQueryElementPresent(self,csPath="",_timeout=2_0000):

        try:
            self.page.wait_for_selector(csPath,timeout=_timeout)
            objElement=self.page.query_selector(csPath)
            if objElement is not None:
                return True
        except PlaywrightTimeoutError as ex:
            return False
    def queryElementClick(self,csPath=""):
        try:
            if self.isQueryElementPresent(csPath):
                self.page.query_selector(csPath).click()
        except PlaywrightTimeoutError as ex:
            print(f"Error {ex}")

    def snImpersonatedUser(self,user_name=""):
        try:

            avatar_button = "macroponent-f51912f4c700201072b211d4d8c26010 div.header-avatar-button"
            if self.isQueryElementPresent(avatar_button,_timeout=1_0000):
                self.page.query_selector(avatar_button).click()
            if user_name:
                xpath="macroponent-f51912f4c700201072b211d4d8c26010 button.user-menu-button.impersonateUser.keyboard-navigatable.polaris-enabled"
                if self.isQueryElementPresent("macroponent-f51912f4c700201072b211d4d8c26010 button.user-menu-button.impersonateUser.keyboard-navigatable.polaris-enabled",_timeout=5_00):
                    objHtml=self.page.query_selector("macroponent-f51912f4c700201072b211d4d8c26010 button.user-menu-button.impersonateUser.keyboard-navigatable.polaris-enabled")

                    objHtml.click()
            else:


                objHtml = self.page.query_selector(
                    "macroponent-f51912f4c700201072b211d4d8c26010 button.user-menu-button.unimpersonate")
                if self.isQueryElementPresent("macroponent-f51912f4c700201072b211d4d8c26010 button.user-menu-button.unimpersonate"):
                    objHtml.click()
                else:
                    self.page.query_selector("macroponent-f51912f4c700201072b211d4d8c26010 div.now-modal-footer button slot span.now-line-height-crop").click()
        except PlaywrightTimeoutError as ex:
            print("Impersonated time out error")
    def isPortalImpersonated(self,user):
        self.click_element(locator="//ul[@class='nav navbar-nav ng-scope']//a[@id='profile-dropdown']")
        if self.isElementPresent(locator="//ul[@class='dropdown-menu']//li//a[text()='End Impersonation']"):
            self.click_element(locator="//ul[@class='dropdown-menu']//li//a[text()='End Impersonation']")

    def isImpersonated(self,user):
        _isimpersonated=False

        self.snImpersonatedUser(user)
        txt_imp=self.page.locator("div.impersonation input.now-typeahead-native-input[placeholder='Search for a user']")
        if self.isQueryElementPresent("div.impersonation input.now-typeahead-native-input[placeholder='Search for a user']"):
            txt_imp.fill(user)




        if self.isQueryElementPresent(f"seismic-hoist mark:text('{user}')",_timeout=5000):

            obj_text=self.page.query_selector(f"seismic-hoist div.now-dropdown-list-sublabel:has-text('{user}')").inner_text()
            if obj_text== user:
                _isimpersonated = True



        return _isimpersonated





    def isElementsPresent(self, locator, loca_type='xpath' ) -> bool:
        try:
            # Use Playwright's `locator` to select all matching elements
            elements = self.page.locator(locator)

            # Check if the count of matching elements is greater than 0
            if elements.count() > 0:
                return True
            else:
                return False

        except PlaywrightTimeoutError as ex:
            #Log(LogType.ERROR, f"isElementsPresent: Error: {str(ex)}")
            return False
    def isElementPresent(self, locator, loca_type='xpath', minimize_wait=False):
        #if minimize_wait:
           # self.minimize_wait()

        return_val = False

        try:
            # Try to locate the element using Playwright's locator system

            element = self.page.locator(locator)
            if minimize_wait:
                element.wait_for(state="visible",timeout=3000)

            # Check if the element is present and visible (using `.is_visible()` method)
            if element.count():
                return_val = True
            else:
                return_val = False

        except PlaywrightTimeoutError as ex:
            # Log(LogType.ERROR, f"isElementPresent: Error: {str(ex)}")
            return_val = False

        #if minimize_wait:
            #self.normalize_wait()

        return return_val

    def take_screenshot_and_upload(self, logIt=True):
        # Implement your screenshot logic here
        pass
    def xpath_to_css(self,xpath):
        # Basic replacement for XPath to CSS conversion
        xpath = xpath.strip()

        # Replace `//` with direct descendant or any descendant selector
        xpath = re.sub(r'^//', '', xpath)  # Remove starting `//`
        # xpath = re.sub(r'/', ' > ', xpath)  # Replace `/` with direct child selector
        xpath = re.sub(r'/', ' ', xpath)  # Replace `/` with direct child selector

        # Replace `[@id="value"]` with `#value`
        xpath = re.sub(r'\[@id=["\']([^"\']+)["\']\]', r'#\1', xpath)

        # Replace `[@class="value"]` with `.value`
        xpath = re.sub(r'\[@class=["\']([^"\']+)["\']\]', r'.\1', xpath)

        # Replace `[@attribute="value"]` with `[attribute="value"]`
        xpath = re.sub(r'\[@([^\]]+)=[\"\']?([^\"\']+)[\"\']?\]', r'[\1="\2"]', xpath)

        # Convert `[text()='value']` to `:contains(value)` (CSS can't match text directly)
        xpath = re.sub(r'\[text\(\)=["\']([^"\']+)["\']\]', r':contains("\1")', xpath)

        # Remove remaining brackets and text() functions (which CSS doesn't support)
        xpath = re.sub(r'text\(\)', '', xpath)

        return xpath.strip()
    def click_element(self, locator, loca_type='xpath', is_retriggered=False):
        try:
            # Select the element based on the locator type
            if loca_type == 'xpath':
                element = self.page.locator(locator)
            elif loca_type=="cspath":
                element= self.page.locator(self.xpath_to_css(locator))
            else:
                # Handle other locator types if necessary
                raise ValueError("Unsupported locator type")

            if element.count() > 0:  # Check if the element exists
                element.click()
            else:
                print(
                    f"Not clicked. Element object is false. with locator :: {locator} and Locator type :: {loca_type}")

        except Exception as ex:
            print(f"Not Clicked on Element with locator :: {locator} and Locator type :: {loca_type}, Error: {str(ex)}")

            if "Other element would receive the click" in str(ex):
                if not is_retriggered:
                    self.take_screenshot_and_upload(logIt=False)

                if not is_retriggered and ('class="help4-content"' in str(ex) or 'class="help4-' in str(ex)):
                    self.click_element("(//button[contains(@class,'help4-close')])[2]", 'xpath', is_retriggered=True)
                    self.click_element("(//button[contains(@class,'help4-close')])[1]", 'xpath', is_retriggered=True)
                    self.click_element(locator, loca_type, is_retriggered=True)

    def impersonate_user(self, userName) -> bool:
        is_impersonated=False
        usermenu_XPath = '//div[@data-id="user-menu"]'
        if self.isElementsPresent(usermenu_XPath,loca_type="xpath"):
            self.click_element(usermenu_XPath)
            impersonateuser_opt = '//sn-contextual-menu[@id="userMenu"]//button[contains(@class,"impersonateUser")]'
            impersonateuser_input = '//sn-impersonation//div[@class="impersonation"]//input'

            user_dd_list = '//seismic-hoist//div[@class="now-dropdown-list"]//div[@role="option"]//div[@class="now-dropdown-list-sublabel"]'
            user_path = f'//seismic-hoist//div[@class="now-dropdown-list"]//div[@role="option"]//div[@username="{userName}"]'
            ImpersonateUser_Btn = '//sn-impersonation//div[@class="now-modal-footer"]//button[@type="button"]//slot//span'
            if self.isElementPresent(impersonateuser_opt):
                self.click_element(impersonateuser_opt)
                wait_Custom(0.4)
                self.page.locator(impersonateuser_input).fill(userName)

    def xpath_to_css(self,xpath):
        # Basic replacement for XPath to CSS conversion
        xpath = xpath.strip()

        # Replace `//` with direct descendant or any descendant selector
        xpath = re.sub(r'^//', '', xpath)  # Remove starting `//`
        # xpath = re.sub(r'/', ' > ', xpath)  # Replace `/` with direct child selector
        xpath = re.sub(r'/', ' ', xpath)  # Replace `/` with direct child selector

        # Replace `[@id="value"]` with `#value`
        xpath = re.sub(r'\[@id=["\']([^"\']+)["\']\]', r'#\1', xpath)

        # Replace `[@class="value"]` with `.value`
        xpath = re.sub(r'\[@class=["\']([^"\']+)["\']\]', r'.\1', xpath)

        # Replace `[@attribute="value"]` with `[attribute="value"]`
        xpath = re.sub(r'\[@([^\]]+)=[\"\']?([^\"\']+)[\"\']?\]', r'[\1="\2"]', xpath)

        # Convert `[text()='value']` to `:contains(value)` (CSS can't match text directly)
        xpath = re.sub(r'\[text\(\)=["\']([^"\']+)["\']\]', r':contains("\1")', xpath)

        # Remove remaining brackets and text() functions (which CSS doesn't support)
        xpath = re.sub(r'text\(\)', '', xpath)

        return xpath.strip()
    def serviceNowLogin(self,user_name,pwd):
            txt_login = self.page.locator("id=user_name")
            txt_pwd = self.page.locator("id=user_password")
            txt_login.fill(credentials.sn_user_name)
            txt_pwd.fill(credentials.sn_user_pwd)

            if self.isElementsPresent("//button[text()='Log in']",5_00):
                self.click_element("//button[text()='Log in']")

    def take_screenshot_and_save(self, folder_path, file_name="screenshot.png"):
        # Ensure the folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Define full path for the screenshot
        file_path = os.path.join(folder_path, file_name)

        # Take screenshot and save it
        self.page.screenshot(path=file_path)
        print(f"Screenshot saved at: {file_path}")

