from pages.base_page import BasePage
from pages.locators.locators_home_page import HomePageConstants as home_const
from pages.locators.base_locators import ButtonLocators as btn


class HomePage(BasePage):

    def __init__(self, page, base_url, locale="en"):
        self.page = page
        self.base_url = base_url
        self.locale = locale

    def open_page(self):
        self.open_url(self.base_url)

    def click_go_to_records(self):
        go_to_records = self.get_by_role(btn.BUTTON, name=home_const.GO_TO_RECORDS_TEXT)
        go_to_records.click()


