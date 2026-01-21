from playwright.sync_api import Page


class BasePage:

    def __init__(self, page: Page, base_url):
        self.page = page
        self.base_url = base_url

    def open_url(self, base_url):
        self.page.goto(base_url)

    def get_locator(self, locator):
        return self.page.locator(locator)

    def get_by_role(self, role, **kwargs):
        return self.page.get_by_role(role, **kwargs)

    def click_element(self, locator):
        element = self.get_locator(locator)
        element.wait_for(state="visible")
        element.click()

