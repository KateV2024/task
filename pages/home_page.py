from pages.base_page import BasePage


class HomePage(BasePage):

    WELCOME_HEADING = "heading"
    WELCOME_TEXT = "Welcome!"
    GO_TO_RECORDS_BUTTON = "button"
    GO_TO_RECORDS_TEXT = "Go to Records"

    def __init__(self, page, base_url, locale="en"):
        self.page = page
        self.base_url = base_url
        self.locale = locale

    def get_home_page(self):
        self.open_url(self.base_url)

    def check_go_to_records_btn_exist(self):
        return self.get_by_role(self.GO_TO_RECORDS_BUTTON, name = self.GO_TO_RECORDS_TEXT)

    def click_go_to_records(self):
        self.check_go_to_records_btn_exist().click()


